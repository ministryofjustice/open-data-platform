def globals(request):
  return {
    'app_title': 'MOJ Open Data Platform', # Application Title (Populates <title>)
    'proposition_title': 'MOJ Open Data Platform', # Proposition Title (Populates proposition header)
    'phase': 'alpha', # Current Phase (Sets the current phase and the colour of phase tags). Presumed values: alpha, beta, live
    'product_type': 'information', # Product Type (Adds class to body based on service type). Presumed values: information, service
    'feedback_url': '/feedback', # Feedback URL (URL for feedback link in phase banner)
    'ga_id': '' # Google Analytics ID (Tracking ID for the service)
  }
