from datatypes.validators.iso_country_code_validator import countries

countries_list_for_selector = map(lambda x: (x.alpha2, x.name), countries)
