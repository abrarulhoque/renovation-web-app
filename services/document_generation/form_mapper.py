from typing import Dict, Any
from forms.renovation_form import RenovationForm
from calculations.cost_calculations import (
    calculate_labor_cost,
    calculate_material_cost,
    calculate_waste_cost,
    calculate_discount,
    calculate_total,
    calculate_rot_deduction,
    calculate_labor_cost_option1,
    calculate_material_cost_option1,
    calculate_waste_cost_option1,
    calculate_discount_option1,
    calculate_total_option1,
    calculate_rot_deduction_option1,
    calculate_labor_cost_option2,
    calculate_material_cost_option2,
    calculate_waste_cost_option2,
    calculate_discount_option2,
    calculate_total_option2,
    calculate_rot_deduction_option2,
)


class FormMapper:
    """
    Maps form data to Word template variables.
    """

    @staticmethod
    def map_personal_details(form: RenovationForm) -> Dict[str, Any]:
        """
        Maps personal details from the form to template variables.

        Args:
            form: The submitted form with data

        Returns:
            Dictionary with mapped template variables
        """
        return {
            "name": form.personal_details.first_name.data
            + " "
            + form.personal_details.last_name.data,
            "ePost": form.personal_details.email.data,
            "telefon": form.personal_details.phone.data,
            "address": form.personal_details.address.data,
        }

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
                # === Always included items (standard in any renovation) ===
                "etablering": "Etablering",  # Always included
                "tacka_golv": "Täcka golv",  # Always included
                "tacka_dorropningar": "Täcka dörröppningar",  # Always included
                "stanga_koppla_el": "Stänga av och koppla el",  # Always included
                "nedmontering_badrumsinredning": "Nedmontering av badrumsinredning",  # Always included
                "rivning_ytskikt": "Rivning ytskikt",  # Always included
                "inbarning_byggmaterial": "Inbärning byggmaterial",  # Always included
                "gipsvaggar_plywood": "Gipsväggar med plywood",  # Always included
                "spackling": "Spackling",  # Always included
                "gjutning_golvspackling": "Gjutning och golvspackling",  # Always included
                "applicering_tatskikt": "Applicering tätskikt",  # Always included
                "plattsattning": "Plattsättning",  # Always included
                "satting_hornlister": "Sättning hörnlister",  # Always included
                "applicering_fog_silikon": "Applicering fog och silikon",  # Always included
                "utanpaliggande_tappvatten": "Utanpåliggande tappvatten",  # Always included
                "sortera_byggsopor": "Sortera byggsopor",  # Always included
                # === Conditional items based on form values ===
                # Bathroom components and modifications
                "golvet_bilas": (
                    "Golvet bilas"
                    if form.interior_fittings.bathtub_normal.data
                    or form.interior_fittings.bathtub_long.data
                    else ""
                ),
                "proppa_avlopp": (
                    f"Proppa gamla avlopp ({form.bathroom_details.floor_drain_relocation.data} st)"
                    if form.bathroom_details.floor_drain_relocation.data
                    and form.bathroom_details.floor_drain_relocation.data != "0"
                    else ""
                ),
                "taket_sanks": (
                    "Taket sänks" if form.appliances.ceiling_lowering.data else ""
                ),
                "grovstadning": (
                    "Grovstädning" if form.tiles_and_painting.cleanup.data else ""
                ),
                # Specific installations
                "el_buren_golvvarme": (
                    "Elektrisk golvvärme" if form.appliances.floor_heating.data else ""
                ),
                "kommod": (
                    "Tvättställskommod"
                    if form.interior_fittings.vanity_unit.data
                    else ""
                ),
                "tvattstall": (
                    "Tvättställ" if form.interior_fittings.vanity_unit.data else ""
                ),
                "tvattstallsblandare": (
                    "Tvättställsblandare"
                    if form.interior_fittings.vanity_unit.data
                    else ""
                ),
                "spegel_belysning": (
                    "Spegel med belysning"
                    if form.interior_fittings.mirror_lighting.data
                    else ""
                ),
                "badrumskap": (
                    "Spegelskåp med belysning"
                    if form.interior_fittings.mirror_cabinet.data
                    else ""
                ),
                "duschset": (
                    "Duschblandare med handdusch"
                    if form.interior_fittings.shower_mixer.data
                    else ""
                ),
                "duschvaggar": (
                    "Glasduschvägg"
                    if form.interior_fittings.glass_shower_wall.data
                    else (
                        "Duschvägg"
                        if form.interior_fittings.shower_wall.data
                        else (
                            "Glasblockvägg"
                            if form.interior_fittings.glass_block_wall.data
                            else (
                                "Duschdörrar"
                                if form.interior_fittings.shower_doors.data
                                else ""
                            )
                        )
                    )
                ),
                "toalett": (
                    "Väggmonterad toalett"
                    if form.interior_fittings.toilet_wall_mounted.data
                    else (
                        "Fristående toalett"
                        if form.interior_fittings.toilet_freestanding.data
                        else ""
                    )
                ),
                "handduktork": (
                    "Elektrisk handdukstork"
                    if form.appliances.electric_towel_warmer.data
                    else ""
                ),
                "tvattmaskin": (
                    "Tvättmaskin" if form.appliances.washing_machine.data else ""
                ),
                "spotlights": (
                    f"Spotlights ({form.appliances.spotlights_count.data} st)"
                    if form.appliances.spotlights_count.data
                    and form.appliances.spotlights_count.data > 0
                    else ""
                ),
                "flakt": (
                    "Takfläkt/Ventilation"
                    if form.appliances.ceiling_lowering.data
                    else ""
                ),
                "el_uttag": (
                    "Elkontakter (flera)"
                    if (
                        form.appliances.sink_outlet.data
                        and form.appliances.iron_outlet.data
                    )
                    else (
                        "Elkontakt vid tvättställ"
                        if form.appliances.sink_outlet.data
                        else (
                            "Elkontakt för strykjärn"
                            if form.appliances.iron_outlet.data
                            else "Vägguttag" if form.appliances.wall_socket.data else ""
                        )
                    )
                ),
                # Additional details from form
                "service_bil": (
                    f"Service bil ({form.personal_details.service_car_days.data} dagar, {form.personal_details.service_car_price.data} kr)"
                    if form.personal_details.service_car_days.data
                    and form.personal_details.service_car_price.data
                    else ""
                ),
                "antal_omplaceringar": (
                    f"Antal omplaceringar: {form.bathroom_details.relocation_count.data}"
                    if form.bathroom_details.relocation_count.data
                    and form.bathroom_details.relocation_count.data != "0"
                    else ""
                ),
                "floor_penetrations": (
                    f"Andra genomföringar från golvet ({form.bathroom_details.floor_penetrations.data} st)"
                    if form.bathroom_details.floor_penetrations.data
                    and form.bathroom_details.floor_penetrations.data != "0"
                    else ""
                ),
                "wall_penetrations": (
                    f"Genomföringar till väggar ({form.bathroom_details.wall_penetrations.data} st)"
                    if form.bathroom_details.wall_penetrations.data
                    and form.bathroom_details.wall_penetrations.data != "0"
                    else ""
                ),
            }
        )

        return options

    @staticmethod
    def map_cost_calculations(form: RenovationForm) -> Dict[str, Any]:
        """
        Maps cost calculations to template variables.

        Args:
            form: The submitted form with data

        Returns:
            Dictionary with mapped template variables
        """
        try:
            # Calculate costs based on form data
            # Main option costs
            labor_cost = calculate_labor_cost(form)
            material_cost = calculate_material_cost(form)
            waste_cost = calculate_waste_cost(form)
            discount = calculate_discount(form)
            rot_deduction = calculate_rot_deduction(form)

            # Calculate labor cost AFTER ROT deduction (this was the key issue in the analysis)
            labor_cost_after_rot = labor_cost - rot_deduction

            total = calculate_total(form)
            final_cost = total - rot_deduction

            # Option 1 costs
            labor_cost_option1 = calculate_labor_cost_option1(form)
            material_cost_option1 = calculate_material_cost_option1(form)
            waste_cost_option1 = calculate_waste_cost_option1(form)
            discount_option1 = calculate_discount_option1(form)
            rot_deduction_option1 = calculate_rot_deduction_option1(form)

            # Calculate labor cost AFTER ROT deduction for option 1
            labor_cost_option1_after_rot = labor_cost_option1 - rot_deduction_option1

            total_option1 = calculate_total_option1(form)
            final_cost_option1 = total_option1 - rot_deduction_option1

            # Option 2 costs
            labor_cost_option2 = calculate_labor_cost_option2(form)
            material_cost_option2 = calculate_material_cost_option2(form)
            waste_cost_option2 = calculate_waste_cost_option2(form)
            discount_option2 = calculate_discount_option2(form)
            rot_deduction_option2 = calculate_rot_deduction_option2(form)

            # Calculate labor cost AFTER ROT deduction for option 2
            labor_cost_option2_after_rot = labor_cost_option2 - rot_deduction_option2

            total_option2 = calculate_total_option2(form)
            final_cost_option2 = total_option2 - rot_deduction_option2

            # Map cost variables to template
            cost_variables = {
                # Main option costs for Fast Pris section - use labor AFTER ROT deduction
                "arbetskostnad_main": labor_cost_after_rot,  # FIXED: now using after ROT value
                "materialkostnad_main": material_cost,
                "avfallshantering_main": waste_cost,
                "rabatt_main": discount,
                "total_sum_main": total,
                "rot_avdrag_main": rot_deduction,
                "slutkostnad_main": final_cost,
                # Option 1 costs - use labor AFTER ROT deduction
                "arbetskostnad_option1": labor_cost_option1_after_rot,  # FIXED: now using after ROT value
                "materialkostnad_option1": material_cost_option1,  # Use correct name for the template
                "byggmaterial_option1": material_cost_option1,  # Alternative name used in template
                "avfallshantering_option1": waste_cost_option1,
                "rabatt_option1": discount_option1,
                "total_sum_option1": total_option1,
                "rot_avdrag_option1": rot_deduction_option1,
                "slutkostnad_option1": final_cost_option1,
                # Option 2 costs - use labor AFTER ROT deduction
                "arbetskostnad_option2": labor_cost_option2_after_rot,  # FIXED: now using after ROT value
                "materialkostnad_option2": material_cost_option2,  # Use correct name for the template
                "byggmaterial_option2": material_cost_option2,  # Alternative name used in template
                "avfallshantering_option2": waste_cost_option2,
                "rabatt_option2": discount_option2,
                "total_sum_option2": total_option2,
                "rot_avdrag_option2": rot_deduction_option2,
                "slutkostnad_option2": final_cost_option2,
                # Format costs as strings with SEK currency for display
                "arbetskostnad_main_str": f"{labor_cost_after_rot:,.2f} kr",  # FIXED: now using after ROT value
                "materialkostnad_main_str": f"{material_cost:,.2f} kr",
                "avfallshantering_main_str": f"{waste_cost:,.2f} kr",
                "rabatt_main_str": f"{discount:,.2f} kr",
                "total_sum_main_str": f"{total:,.2f} kr",
                "rot_avdrag_main_str": f"{rot_deduction:,.2f} kr",
                "slutkostnad_main_str": f"{final_cost:,.2f} kr",
                # Additional template variables that match the Word document
                "labor_cost": f"{labor_cost_after_rot:,.2f}",  # FIXED: now using after ROT value
                "material_cost": f"{material_cost:,.2f}",
                "waste_cost": f"{waste_cost:,.2f}",
                "discount": f"{discount:,.2f}",
                "total_cost": f"{total:,.2f}",
                "rot_deduction": f"{rot_deduction:,.2f}",
                "final_cost": f"{final_cost:,.2f}",
                "option1_cost": f"{total_option1:,.2f}",
                "option2_cost": f"{total_option2:,.2f}",
            }

            return cost_variables

        except Exception as e:
            # Log the error and return empty values
            print(f"Error calculating costs: {str(e)}")
            return {
                "labor_cost": "0",
                "material_cost": "0",
                "waste_cost": "0",
                "discount": "0",
                "total_cost": "0",
                "rot_deduction": "0",
                "final_cost": "0",
                "option1_cost": "0",
                "option2_cost": "0",
            }

    @staticmethod
    def map_form_to_template(form: RenovationForm) -> Dict[str, Any]:
        """
        Maps the entire form to template variables.

        Args:
            form: The submitted form with data

        Returns:
            Dictionary with all mapped template variables
        """
        # Start with personal details
        context = FormMapper.map_personal_details(form)

        # Add renovation options
        context.update(FormMapper.map_renovation_options(form))

        # Add cost calculations
        context.update(FormMapper.map_cost_calculations(form))

        return context
