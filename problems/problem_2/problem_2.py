from flask import Response, jsonify

def test_problem_2(data: dict) -> tuple:
    return jsonify({"error": "Not implemented"}), 501