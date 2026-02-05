#!/usr/bin/env python3

#-------------------------------------------------------------------------------
# Import Stuff
#-------------------------------------------------------------------------------
from src import app
from flask import request

#-------------------------------------------------------------------------------
# regions()
# Get the regions for the game map
#
# Parameters
# game_map | str | Either "US" or "GB"
#
# Returns
# List of regions
#-------------------------------------------------------------------------------
@app.route( "/api/regions/<string:game_map>" )
def regions( game_map ):
    game_data = app.config[ "data" ]

    try:
        regions = list( game_data[ "maps" ][ game_map ][ "destinations" ][ "cities" ].keys() )
    except KeyError:
        regions = []

    return { "regions": regions }

#-------------------------------------------------------------------------------
# cities()
# Get the cities for the game map
#
# Parameters
# game_map | str | Either "US" or "GB"
#
# Returns
# List of cities
#-------------------------------------------------------------------------------
@app.route( "/api/cities/<string:game_map>" )
def cities( game_map ):
    game_data = app.config[ "data" ]

    try:
        cities = list( game_data[ "maps" ][ game_map ][ "payouts" ].keys() )
    except KeyError:
        cities = []

    return { "cities": cities }

#-------------------------------------------------------------------------------
# payout()
# Calculates the payout of a given route
#
# Parameters
# game_map | str | Either "US" or "GB"
# origin | str | The origin city for the route
# destination | str | The destination city for the route
#
# Returns
# Expected payout for a route
#-------------------------------------------------------------------------------
@app.route( "/api/payout/<string:game_map>/<string:origin>/<string:destination>" )
def payout( game_map, origin, destination ):
    game_data = app.config[ "data" ]

    try:
        payout = game_data[ "maps" ][ game_map ][ "payouts" ][ origin ][ destination ]
    except KeyError:
        payout = "0"

    return { "payout": payout }

#-------------------------------------------------------------------------------
# destinate()
# Determines a destination based on a given roll
#
# Parameters
# None
#
# Returns
# Expected destination based on roll
#-------------------------------------------------------------------------------
@app.route( "/api/destinate", methods = [ "POST" ] )
def destinate():
    #---------------------------------------------------------------------------
    # Get the POST body
    #---------------------------------------------------------------------------
    body = request.get_json()

    #---------------------------------------------------------------------------
    # Get individual parameters from POST body
    #---------------------------------------------------------------------------
    game_map = body[ "map" ]
    destination_type = body[ "type" ]
    odd_even = body[ "odd_even" ]
    roll = body[ "roll" ]

    #---------------------------------------------------------------------------
    # Get our game data
    #---------------------------------------------------------------------------
    game_data = app.config[ "data" ]

    #---------------------------------------------------------------------------
    # If the destination_type is "region" it means we're looking for a region
    # Otherwise we'll treat destination_type as the name of the region we want
    # a city destination in.
    #---------------------------------------------------------------------------
    if destination_type == "region":
        destination = game_data[ "maps" ][ game_map ][ "destinations" ][ "regions" ][ odd_even ][ roll ]
    else:
        destination = game_data[ "maps" ][ game_map ][ "destinations" ][ "cities" ][ destination_type ][ odd_even ][ roll ]

    #---------------------------------------------------------------------------
    # Return the destination
    #---------------------------------------------------------------------------
    return { "destination": destination }
