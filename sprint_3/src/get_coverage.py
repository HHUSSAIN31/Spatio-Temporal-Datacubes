import xml.etree.ElementTree as ET
import requests
from .type_request import type_request

def formatText(string: str) -> str:
    """
    Formats a give string by eliminating every character
    until the first met '}' character.
    
    :param string: str variable to be formatted.

    :return: formatted string.

    :raise: ValueError if another type than str is given.
    """

    if isinstance(string, str) :
        return string[string.find('}') + 1:]
    else:
        raise ValueError("Expected str type variable.")

def isBlank(string : str) -> bool:
    """
    Checks whether a string is empty (blank) or not.

    :param string: str variable to be checked.

    :return: boolean value whether the string is blank or not.

    :raise: ValueError if another type than str is given.
    """
    if isinstance(string, str) :
        for char in string:
            if (char != ' '  and
                char != '\t' and
                char != '\n' and
                char != '\r'):
                return False
        return True
    else:
        raise ValueError("Expected str type variable.")

def getAvailableRequests(
        url : str ="https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities",
        statusUpdates: bool = False) -> list:
    """
    Makes a get request to the provided url, expecting an xml response.
    Creates a .debug.xml file to store server's response if the
    status_code == 200 in order to be able to trace back any errors.
    Afterwards, the response's content will further more be processed
    into a list of lists which will be the value returned.
    
    :param url: server's url from where to request coverages using a get request.
    :param statusUpdates: boolean variable based on which extra status updates
        on the standard output will be shared.
    :return: processed server's response into a list of lists or
        an empty list if anything went wrong.
    
    :raise: ValueError if another type than str is given for url.
    :raise: ValueError if another type than bool is given for statusUpdates.
    """
    if not isinstance(url, str):
        raise ValueError("Expected str type variable for url.")
    if not isinstance(statusUpdates, bool):
        raise ValueError("Expected bool, int type variable for statusUpdates.")

    if statusUpdates:
        print("Requesting data from: '", url, "'", sep='')

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        if statusUpdates:
            print(f"Request err: {e}")
        return []
    
    if (response.status_code != 200):
        print("Server Connection Failed:", response.status_code)
        return []
    if statusUpdates:
        print("Request was successful!")

    if statusUpdates:
        print("Creating debug file: '.debug.xml'")
    file = open('.debug.xml', 'w')
    file.write(response.text)
    file.close()
    if statusUpdates:
        print("'.debug.xml' was successfully created!")
        print("Processing file...")

    try:
        tree = ET.parse('.debug.xml')
        root = tree.getroot()
        data = []
        data_sub = []
        temp = []
    except Exception as e:
        if statusUpdates:
            print("Unexpected file format.")
        return []


    for content in root:
        if ("Contents" in content.tag):
            for tags in content:
                data_sub = []
                for tag in tags:
                    if isBlank(tag.text) == False:
                        data_sub.append(tag.text)
                    if tag:
                        temp = []
                        if ("AdditionalParameters" not in tag.tag):
                            for info in tag:
                                temp.append(info.text)
                        else:
                            for additional in tag:
                                for info in additional:
                                    temp.append(info.text)
                        data_sub.append(temp)
                data.append(data_sub)
    
    if statusUpdates:
        print("Done processing!")

    return data

def processedDataIntoList(
        url : str ="https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities",
        statusUpdates: bool = False) -> tuple[type_request, int]:
    """
    Requests and formats data into type_request objects
    from a certain url based on its expected incoming format.

    :param url: server's url from where to request coverages using a get request.
    :param statusUpdates: boolean variable based on which extra status updates
        on the standard output will be shared.
    :return: tuple[processedRequests, ignoredRequests]

    :raise: ValueError if another type than str is given for url.
    :raise: ValueError if another type than bool, int is given for statusUpdates.
    """
    if not isinstance(url, str):
        raise ValueError("Expected str type variable for url.")
    if not isinstance(statusUpdates, (bool, int)):
        raise ValueError("Expected bool, int type variable for statusUpdates.")

    # initialising data accordingly to their use case.
    # *data* will hold the raw response of the server's response.
    data = []
    data = getAvailableRequests(url, statusUpdates)
    availableRequsts = []
    ignored = 0

    if statusUpdates:
        print("Formatting data...")

    # attempting format data into type_request variables
    for type in data:
        if len(type) == 5:
            availableRequsts.append(type_request(type[0],
                                                type[1],
                                                type[2],
                                                type[3],
                                                type[4]))
        elif len(type) == 6:
            availableRequsts.append(type_request(type[0],
                                                type[1],
                                                type[3],
                                                type[4],
                                                type[5],
                                                type[2]))
        elif len(type) == 4:
            availableRequsts.append(type_request(type[0],
                                                type[1],
                                                type[2],
                                                type[3]))
        else:
            ignored += 1
    
    if statusUpdates:
        print("Done formatting!")


    return availableRequsts, ignored
