import re

class type_request:
    """
    A class to store request structured information.
    As of now it has an initialising function: __init__, with 
    multiple parameters that can be set: id, coverageType,
    bounds_1, bounds_2, additionalParameters, coverageTypeExtended,
    service_endpoint, serviceType, serviceVersion and request.
    Moreover, it has full comparison support, in order to
    order a list / lists of multiple type_request objects.

    :param id: A string containing the id.
    :param coverageType: A string containing a coverage_type.
    :param coverageTypeExt: A list containing any additional coverage_type information.
    :param bounds_1: A list containing core bounds (usually lower).
    :param bounds_2: A list containing core bounds (usually upper).
    :param additionalParams: A list of lists of any additional parameters.
        it usually includes better defined information about bounds,
        by specifying their type (whether it's lat or lon for example).
    :param serverRequest: A special space for a string containing a pre-process request.
    :param service_endpoint: A string containing the server's endpoint. Can be used
        for both debug and server_request creation.
    :param serviceType: A string containing the service_type of
        the possible request. With the purpose of supporting pre-processing
        requests / independent (class related) request creation.
    :param serviceVersion: A string containing the server's service_version, with
        the meaning the same as above.
    :param request: A string containing the actual request, that is would be
        ready to be executed, with the same meaning of pre-processing
        and to avoid any over-processing if the same request were to
        be executed over and over.
    :param extracted_bounds_dict: A dictionary of a list containing extracted
        information of any successfull extracted bounds on the axis_list.
    :param encode_format: A string with the purpose of serving the above mentioned
        functionality of generating the request. Containing a format, ex: "img/png".

    :raise: ValueError if any of the parameter's type are wrongfully given.
    """
    id: str
    coverageType: str
    coverageTypeExt: list
    bounds_1: list
    bounds_2: list
    additionalParams: list
    serverRequest: str
    service_endpoint: str # "https://ows.rasdaman.org/rasdaman/ows"
    serviceType: str # "WCS"
    serviceVersion: str # "2.1.0"
    request: str # "GetCoverage"
    extracted_bounds_dict: dict[list] # supported types: 'lat', 'lon', 'e', 'n', 'date'
                                      # and whatever else might be, in raw format
    encode_format: str # "image/png"

    def __init__(self,
                 id: str = "unset",
                 coverageType: str = "unset",
                 bounds_1: list = ["unset", "unset"],
                 bounds_2: list = ["unset", "unset"],
                 additionalParameters: list = [["unset", "unset"]],
                 coverageTypeExtended: list = [],
                 service_endpoint: str = "https://ows.rasdaman.org/rasdaman/ows",
                 serviceType: str = "WCS",
                 serviceVersion: str = "2.1.0",
                request: str = ""
                ) -> None:
        """Initializes the object"""
        if not isinstance(id, str)\
           or not isinstance(coverageType, str)\
           or not isinstance(bounds_1, list)\
           or not isinstance(bounds_2, list)\
           or not isinstance(additionalParameters, list)\
           or not isinstance(coverageTypeExtended, list)\
           or not isinstance(service_endpoint, str)\
           or not isinstance(serviceType, str)\
           or not isinstance(serviceVersion, str)\
           or not isinstance(request, str):
            raise ValueError("wrong parameters' type")
        
        self.id = id
        self.coverageType = coverageType
        self.bounds_1 = bounds_1
        self.bounds_2 = bounds_2
        self.extracted_bounds_dict = dict()
        temp = []
        # checking whether the list of additional parameters is odd by any chance,
        # in which case that would be wrong and a special case to handle this will
        # run instead
        if len(additionalParameters) % 2 == 0:
            for i in range(0, len(additionalParameters), 2):
                # adding additional parameters as key, value pais
                temp.append([additionalParameters[i], additionalParameters[i + 1]])
                
                # attempting to extract key information to be later on used from
                # additional parameters information. Targeted info is everything
                # on the axisList, for example but not limited to: lat, lon, time.
                # 
                if str(additionalParameters[i]).lower() == "axislist":
                    try:
                        temp_bounds_ids = str(additionalParameters[i + 1]).split(',')
                        temp_bounds_specs_1 = str(self.bounds_2[0]).split(' ')
                        temp_bounds_specs_2 = str(self.bounds_2[1]).split(' ')

                        # if the lists don't have the same length after splitting,
                        # an unexpected error occured, most likely a server
                        # response formatting error / data corrupution.
                        if len(temp_bounds_ids) != len(temp_bounds_specs_1)\
                            or len(temp_bounds_ids) != len(temp_bounds_specs_2):
                            continue
                        for index in range(0, len(temp_bounds_ids)):
                            lst = []
                            temp_id_lower = temp_bounds_ids[index].lower()
                            if "ansi" in temp_id_lower\
                                or "time" in temp_id_lower:
                                # using regex expressions to extract dates from a string.
                                date_low = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", temp_bounds_specs_1[index])
                                date_up  = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", temp_bounds_specs_2[index])
                                if date_low and date_up:
                                    lst.append(date_low.string[date_low.start():date_low.end()])
                                    lst.append(date_up.string[date_up.start():date_up.end()])
                                    lst.append(temp_bounds_ids[index])
                                    self.extracted_bounds_dict['date'] = lst
                            elif "lat" in temp_id_lower or "e" in temp_id_lower:
                                lst.append(temp_bounds_specs_1[index])
                                lst.append(temp_bounds_specs_2[index])
                                lst.append(temp_bounds_ids[index])
                                self.extracted_bounds_dict['coord_1'] = lst
                            elif "lon" in temp_id_lower or "n" in temp_id_lower:
                                lst.append(temp_bounds_specs_1[index])
                                lst.append(temp_bounds_specs_2[index])
                                lst.append(temp_bounds_ids[index])
                                self.extracted_bounds_dict['coord_2'] = lst
                            else:
                                lst.append(temp_bounds_specs_1[index])
                                lst.append(temp_bounds_specs_2[index])
                                lst.append(temp_bounds_ids[index])
                                self.extracted_bounds_dict[temp_id_lower] = lst
                    except:
                        # will not actually do anything if something goes wrong
                        # as this is not core for the algorithm to function
                        # raise(f"in type_req __init_ while extracting bounds: {e}")
                        continue
        else:
            for i in range(0, len(additionalParameters) - 1, 2):
                temp.append([additionalParameters[i], additionalParameters[i + 1]])
            temp.append([additionalParameters[len(additionalParameters) - 1],
                                    "undefined"])
        self.additionalParams = temp
        self.coverageTypeExt = coverageTypeExtended

        self.service_endpoint = service_endpoint
        self.serviceType = serviceType
        self.serviceVersion = serviceVersion
        self.request = request

        # could be used to store desired format
        self.encode_format = ""

    def __str__(self) -> str:
        """Returns what to be printed when trying to print an object of this type"""
        val = ""
        it  = 0
        val += "id:                     " + self.id + '\n'
        val += "coverageType:           " + self.coverageType
        if self.coverageTypeExt != []:
            val += ", "
            for txt in self.coverageTypeExt:
                val += str(txt)
        else:
            val += '\n'
        val += "WGSBounds, LowerCorner: " + self.bounds_1[0] + '\n'
        val += "            UperCorner: " + self.bounds_1[1] + '\n'
        val += "Bounds, LowerCorner:    " + self.bounds_2[0] + '\n'
        val += "         UperCorner:    " + self.bounds_2[1] + '\n'
        for pair in self.additionalParams:
            it += 1
            if pair[0] and pair[1]:
                val += "Additional_" + str(it) + ", Name:     " + str(pair[0]) + '\n'
                val += "           " + str(it) + " Value:     " + str(pair[1]) + '\n'
            else:
                val += "Additional_" + str(it) + ", Name:     " + "internalError" + '\n'
                val += "           " + str(it) + " Value:     " + "internalError" + '\n'
            
        if val[len(val) - 1] == '\n':
            val = val[:-1]

        return val

    def __lt__(self, other) -> bool:
        """
        Implementation of comaprison sign: '<'
        
        :raise: ValueError if other is of any other type than type_request.
        """
        if not isinstance(other, type_request):
            raise ValueError("Comparison with other object types, than itself, not supported.")

        if (self.coverageType != other.coverageType):
            return self.coverageType < other.coverageType
        else:
            if len(self.id) != len(other.id):
                return len(self.id) < len(other.id)
            else:
                return self.id < other.id

    def __le__(self, other)  -> bool:
        """
        Implementation of comaprison sign: '<='
        
        :raise: ValueError if other is of any other type than type_request.
        """
        if not isinstance(other, type_request):
            raise ValueError("Comparison with other object types, than itself, not supported.")

        if (self.coverageType != other.coverageType):
            return self.coverageType < other.coverageType
        else:
            if len(self.id) != len(other.id):
                return len(self.id) <= len(other.id)
            else:
                return self.id <= other.id

    def __gt__(self, other) -> bool:
        """
        Implementation of comaprison sign: '>'
        
        :raise: ValueError if other is of any other type than type_request.
        """
        if not isinstance(other, type_request):
            raise ValueError("Comparison with other object types, than itself, not supported.")

        if (self.coverageType != other.coverageType):
            return self.coverageType > other.coverageType
        else:
            if len(self.id) != len(other.id):
                return len(self.id) > len(other.id)
            else:
                return self.id > other.id

    def __ge__(self, other) -> bool:
        """
        Implementation of comaprison sign: '>='
        
        :raise: ValueError if other is of any other type than type_request.
        """
        if not isinstance(other, type_request):
            raise ValueError("Comparison with other object types, than itself, not supported.")

        if (self.coverageType != other.coverageType):
            return self.coverageType > other.coverageType
        else:
            if len(self.id) != len(other.id):
                return len(self.id) >= len(other.id)
            else:
                return self.id >= other.id

    def __eq__(self, other) -> bool:
        """
        Implementation of comaprison sign: '=='
        
        :raise: ValueError if other is of any other type than type_request.
        """
        if not isinstance(other, type_request):
            raise ValueError("Comparison with other object types, than itself, not supported.")

        return self.id == other.id
