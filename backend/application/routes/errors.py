from flask import Blueprint, jsonify

err = Blueprint('errors', __name__ , template_folder='../../templates')


@err.app_errorhandler(404)
def page_not_found(e):
	return jsonify({'MyStatus':'error', 'Message':'Global page not found'}), 404


@err.app_errorhandler(500)
def interval_server_error(e):
    return jsonify({'MyStatus':'error', 'Message':'Global interval server error'}), 500

@err.app_errorhandler(405)
def method_not_allowed(e):
    return jsonify({'MyStatus':'error', 'Message':'The method is not allowed for the requested URL.'}), 405

# errorhandler: Registers an error handler specific to the blueprint. This means the handler will only be called for errors that occur within the routes of that blueprint.

# app_errorhandler: Registers a global error handler for the entire application. This means the handler will be called for errors that occur in any part of the application, regardless of the blueprint.



