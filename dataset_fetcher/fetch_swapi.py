import requests


class FetchSwapi:
    base_url = 'https://swapi.co/api/'
    people_url = base_url + 'people/'
    planets_url = base_url + 'planets/'

    def convert_list_to_dict_with_url_as_key(self, planets):
        planets_with_url_as_key = {}
        for planet in planets:
            planets_with_url_as_key[planet['url']] = planet
        return planets_with_url_as_key

    def get_resolved_peoples(self):
        """Resolved mean that field with url are transformed into field name e.g:
        Resolve the `homeworld` url​field into the homeworld's name
        """

        peoples = self.get_peoples()
        planets_with_url_as_key = self.convert_list_to_dict_with_url_as_key(self.get_planets())

        for people in peoples:
            people['homeworld'] = planets_with_url_as_key[people['homeworld']]['name']

        return peoples

    def get_peoples(self):
        return self.get_all_objects(self.people_url)

    def get_planets(self):
        return self.get_all_objects(self.planets_url)

    def get_all_objects(self, url):
        objects = []

        while url:
            response = requests.get(url).json()
            objects.extend(response['results'])
            url = response['next']

        return objects
