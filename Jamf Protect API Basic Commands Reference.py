#!/usr/bin/env python
import requests
import json

clientID = ''
password = ' '
protectInstance = "" 
"""———————————————————————————————————————"""
"""This file is just a basic command refernce for the Jamf Protect API
I would like to note that we do already have official Python scripts on the Jamf GitHub for Protect
https://github.com/jamf/jamfprotect/tree/main/jamf_protect_api/scripts/python
Take a look at those bad boys to make sure you don't reinvent the wheel
Also, this is going to be more rudimentary than those, the token mechanism, for example, is definitely better in
those than you'll see here, this reference is to help make it understandable to newcomers"""
"""———————————————————————————————————————"""

url = f"https://{protectInstance}.protect.jamfcloud.com/"
session = requests.Session()

"""———————————————————————————————————————"""
"""Building on what we did on the Jamf Pro side, we're going to make functions for some of this.
This is mostly from the Jamf GH,
but modifyied to fit my preferred naming scheme and adding things to make it easier to understand"""
"""———————————————————————————————————————"""
def get_access_token(serverURL, client_id, password):
    """Gets a reusable access token to authenticate requests to the Jamf
    Protect API"""
    authDetails = {
        "client_id": client_id,
        "password": password,
    }
    response = session.post(serverURL + "token", json=authDetails)

    """the raise_for_status is basically a better way to ensure that you didn't get a 404 or something.
    It throws a message if you get anything other than a 200-299 response"""
    response.raise_for_status()
    print(f"printing raise_for_status: {response.raise_for_status()}")
 
    responseData = response.json()
    print(response.json())
    print(
        f"Access token granted, valid for {int(responseData['expires_in'] // 60)} minutes."
    )
    """notice it's called an 'access_token' instead of just 'token' like on the Jamf Pro side"""
    print(responseData["access_token"])
    return responseData["access_token"]
token = get_access_token(url, clientID, password)


"""———————————————————————————————————————"""
"""Jamf Protect doesn't use a rest API like Pro does, instead it uses GraphQL so we need to format things quite differently
https://blog.hubspot.com/website/graphql-vs.-rest-api-whats-the-difference-and-which-is-better-for-your-project
So the below is the actual 'query' that we'll submit to the server
This probably could be simplified further, but for now I'm going to leave it as-is since it's getting what I want. This is the first request I've done to GraphQL,
so I won't claim any level of 'this is THE way to do it' knowledge"""
"""———————————————————————————————————————"""
listComputers = """
    query listComputers(
      $page_size: Int
      $next: String
    ) {
      listComputers(
        input: {
          pageSize: $page_size
          next: $next
        }
      ) {
        items {
          uuid
          hostName
          serial
        }
      }
    }
    """

"""———————————————————————————————————————"""
"""Now that we have a query established, we can use it to make an API call"""
"""———————————————————————————————————————"""
def callingTheAPI(queryToSend):
	apiURL = url + "graphql"
	print(apiURL)
	payload = {"query": queryToSend}
	headers = {"Authorization": token}

	response = session.post(apiURL, json=payload, headers=headers)
	print(response)
	print(response.json())
callingTheAPI(listComputers)













