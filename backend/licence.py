class LicenceTool:
    def __init__(self):
        pass

    def licences(self, lics):
        # return a list of available CC licences,
        # assumes the list has more than one material

        if lics['cc_by_nc_nd'] or lics['cc_by_nd']:
            return ["No Recommended Licence"]
        if lics['cc_by_sa']:
            if lics['cc_by_nc'] or lics['cc_by_nc_sa']:
                return ["No Recommended Licence"]
            else:
                return ["CC BY-SA"]
        if lics['cc_by_nc_sa']:
            return ["CC BY-NC-SA"]
        if lics['cc_by_nc']:
            return ["CC BY-NC - Recommended", "CC BY-NC-SA", "CC BY-NC-ND"]
        return ["CC BY - Recommended", "CC BY-SA", "CC BY-NC", "CC BY-ND", "CC BY-NC-SA", "CC BY-NC-ND"]