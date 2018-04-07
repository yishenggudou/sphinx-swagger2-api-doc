#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, codecs, json
from jinja2 import Template


class SwaggerAPIContext(object):
    
    def __init__(self,
                 _swagger_url,
                 _method,
                 _endpoint,
                 _domain,
                 _title,
                 **kwargs):
        self.swagger_api_url = _swagger_url
        self.kwargs = kwargs
        self.domain = _domain
        self.method = _method
        self.endpoint = _endpoint
        self.title = _title
        self.all_content = {}
        self.default_resjsonobject = {}
        self.default_reqjsonobject = {}
        if self.swagger_api_url.startswith("http"):
            self.load_from_http()
        else:
            self.load_from_path()
    
    @property
    def context(self):
        return self.all_content["paths"][self.endpoint][self.method.lower()]
    
    def load_from_http(self):
        response = urllib.request.urlopen(self.swagger_api_url)
        page = response.read()
        page = page.decode('utf-8')
        self.all_content = json.loads(page)
    
    def load_from_path(self):
        with codecs.open(self.swagger_api_url, 'rb+', 'utf8') as fr:
            page = fr.read()
        self.all_content = json.loads(page)
    
    @property
    def real_path(self):
        """
        /users/(int:user_id)/posts/(tag)
        :return:
        """
        from copy import deepcopy
        _ = deepcopy(self.endpoint)
        for p in self.context["parameters"]:
            if p['in'] == "path":
                _ = _.replace("{" + p["name"] + "}", "({type}:{name})".format(**p))
        return _
    
    @property
    def randon_number(self):
        from random import random
        return int(random() * 100)
    
    @property
    def example_path(self):
        """

        :return:
        """
        if self.kwargs.get("example_path"):
            return self.kwargs.get("example_path")
        from copy import deepcopy
        _ = deepcopy(self.endpoint)
        for p in self.context["parameters"]:
            if p['in'] == "path":
                if ["type"] == "string":
                    _ = _.replace("{" + p["name"] + "}", "example_{0}_value".format(p["name"]))
                else:
                    _ = _.replace("{" + p["name"] + "}", "{0}".format(self.randon_number))
        
        querys = list(filter(lambda x: x['in'] == "query", self.context["parameters"]))
        if len(querys) > 0:
            _ = _ + "?"
            for p in querys:
                if p['type'] == 'string':
                    _ += "{name}={value}&".format(value=p.get("default", "example_value"), **p)
                else:
                    _ += "{name}={value}&".format(value=p.get("default", "123"), **p)
        return _.lstrip("&")
    
    @property
    def summary(self):
        """

        :return:
        """
        if self.kwargs.get("summary"):
            return self.kwargs.get("summary")
        if self.context.get("summary"):
            return self.context.get("summary")
        else:
            _ = """"""
            return _
    
    def get_type_by_definition_name(self, definition_name):
        definitions = self.all_content["definitions"]
        return definitions[definition_name].get("type", "object")
    
    def get_json_schema(self, definition_name, obj):
        definitions = self.all_content["definitions"]
        _ = definitions[definition_name].get("properties", {})
        for key, value in _.items():
            if value.get("$ref", False):
                d_name = value["$ref"].split("/")[-1]
                if self.get_type_by_definition_name(d_name) == "object":
                    obj[key] = {}
                    self.get_json_schema(d_name, obj[key])
                else:
                    obj[key] = [{}]
                    self.get_json_schema(d_name, obj[key][0])
            else:
                if (value.get("type") == 'string'):
                    obj[key] = value["type"]
                else:
                    obj[key] = self.randon_number
    
    @property
    def reqjsonobj(self):
        _ = list(
            filter(lambda x: x['in'] == "body" and x.get("schema", {}).get("$ref"), self.context["parameters"]))
        if (len(_) == 1):
            d_name = _[0]["schema"]["$ref"].split("/")[-1]
            if self.get_type_by_definition_name(d_name) == "object":
                sp = {}
                self.get_json_schema(d_name, sp)
            else:
                sp = [{}]
                self.get_json_schema(d_name, sp[0])
            return json.dumps(sp, indent=4)
        else:
            return ""
    
    @property
    def resjsonobj(self):
        """
        
        :return:
        """
        _ = self.context["responses"].get('200', {}).get("schema", {})
        print(_)
        if _.get("type") == "array":
            _ = _["items"]
            d_name = _["$ref"].split("/")[-1]
            if self.get_type_by_definition_name(d_name) == "object":
                sp = [{}]
                self.get_json_schema(d_name, sp[0])
            else:
                sp = [[{}]]
                self.get_json_schema(d_name, sp[0][0])
            return json.dumps(sp, indent=4)
        elif _.get("$ref", False):
            d_name = _["$ref"].split("/")[-1]
            if self.get_type_by_definition_name(d_name) == "object":
                sp = {}
                self.get_json_schema(d_name, sp)
            else:
                sp = [{}]
                self.get_json_schema(d_name, sp[0])
            return json.dumps(sp, indent=4)
        else:
            return ""
    
    @property
    def title_text(self):
        return self.kwargs.get("title_text", '-').strip() * 100
    
    @property
    def example_request(self):
        """

        :return:
        """
        _ = """
        
   **Example request**:
   
   .. sourcecode:: http

      {{method|upper}} {{example_path|safe}} HTTP/1.1
      Host: {{domain|safe}}
      Accept: {%for customer in context.consumes%}{{customer}},{%endfor%}
      {{reqjsonobj|indent(6)}}
      
   **Example response**:
   
   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      {{resjsonobj|indent(6)}}
   
        """
        template = Template(_)
        return template.render(title=self.title,
                               method=self.method,
                               domain=self.domain,
                               context=self.context,
                               resjsonobj=self.resjsonobj,
                               reqjsonobj=self.reqjsonobj,
                               example_path=self.example_path,
                               )
    
    def get_rst_content(self):
        _ = """
{%if title%}
{{title.strip()|safe}}
{{title_text|safe}}
{%endif%}
.. http:{{method|lower}}:: {{real_path|safe}}

   {{summary.strip()|indent(3)}}
   {{kwargs.desc|indent(3)}}

{{example_request|safe}}

{%for query in context.parameters%}{%if query['in'] == 'query' %}
   :query {{query.type}} {{query.name}}: {{query.description}} query parameter `{{query.name}}` is {{query.required and "" or "not"}} required
{%-endif%}{%-endfor%}
   :reqheader Accept: {%for customer in context.consumes%}{{customer}},{%endfor%}
{%for query in context.parameters%}{%if (query['in'] == 'body' and query.get('schema',{}).get("$ref",False)) %}
   :resjsonobj: {{resjsonobj}}
{%-endif%}
{%if (query['in'] == 'body' and query.get('schema',{}).get("$ref",False)) %}
   :reqheader {{query.name}}: {{query.description}}
{%-endif%}
{%-endfor%}
   :reqheader Authorization: optional OAuth token to authenticate
   :resheader Content-Type: {%for produce in context.produces%}{{produce}},{%endfor%}
{%for response_code,response in context.responses.items()%}
   :statuscode {{response_code}}: {{response.description|safe}}
{%-endfor%}
                """
        template = Template(_.lstrip())
        return template.render(title=self.title,
                               method=self.method,
                               real_path=self.real_path,
                               context=self.context,
                               resjsonobj=self.resjsonobj,
                               reqjsonobj=self.reqjsonobj,
                               summary=self.summary,
                               title_text=self.title_text,
                               kwargs=self.kwargs,
                               example_request=self.example_request,
                               example_path=self.example_path)


if __name__ == "__main__":
    o = SwaggerAPIContext("/Users/timgerk/Downloads/api-docs.json",
                          "get",
                          "/odc/v3/databases",
                          "xx.com",
                          "example AP"
                          )
    print(o.get_rst_content())
