# Updated map_renovation_options method
@staticmethod
def map_renovation_options(form: RenovationForm) -> Dict[str, Any]:
    """
    Maps renovation options from the form to template variables.

    Args:
        form: The submitted form with data

    Returns:
        Dictionary with mapped template variables
    """
    # Create a dictionary to store all the renovation options
    options = {}

    # Map bathroom fixtures - using actual task names instead of Ja/Nej
    options.update(
        {
            # Bathroom fixtures
            "el_buren_golvvarme": (
                "Elektrisk golvvärme" if form.appliances.floor_heating.data else ""
            ),
        }
    )

    # Map construction work - using actual task names instead of Ja/Nej
    options.update(
        {
            # Construction work
            "etablering": "Etablering",  # Always included
            "rivning_ytskikt": "Rivning ytskikt",  # Always included
        }
    )

    return options
