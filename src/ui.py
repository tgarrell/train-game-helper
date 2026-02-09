#!/usr/bin/env python3

#-------------------------------------------------------------------------------
# Import Stuff
#-------------------------------------------------------------------------------
import json
from src import app
from flask import Blueprint, render_template, request, redirect, url_for, make_response

#-------------------------------------------------------------------------------
# Home page route
#-------------------------------------------------------------------------------
@app.route('/')
@app.route('/ui')
def home():
    # Check if map is already selected (from cookie)
    selected_map = request.cookies.get('selected_map')
    
    # If map is already selected, redirect to game page
    if selected_map:
        return redirect(url_for('ui_game', game_map=selected_map))
    
    # Otherwise, show the home page to select a map
    return render_template('home.html')

#-------------------------------------------------------------------------------
# Cities page route
#-------------------------------------------------------------------------------
@app.route('/ui/game')
def ui_game():
    game_map = request.args.get('game_map')
    # Validate map parameter
    if game_map not in ['US', 'GB']:
        return "Invalid map", 400
    
    # Set cookie for selected map
    response = make_response(render_template('game.html', game_map=game_map))
    response.set_cookie('selected_map', game_map)
    
    return response
