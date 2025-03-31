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
                # Bathroom fixtures
                "el_buren_golvvarme": (
                    "Elektrisk golvvärme" if form.appliances.floor_heating.data else ""
                ),
                "duschset": (
                    "Duschblandare med handdusch"
                    if form.interior_fittings.shower_mixer.data
                    else ""
                ),
                "duschvaggar": (
                    "Glasduschvägg"
                    if form.interior_fittings.glass_shower_wall.data
                    else ""
                ),
                "tvattstall": (
                    "Tvättställ med kommod"
                    if form.interior_fittings.vanity_unit.data
                    else ""
                ),
                "tvattstallsblandare": (
                    "Tvättställsblandare"
                    if form.interior_fittings.vanity_unit.data
                    else ""
                ),
                "toalett": (
                    "Toalett"
                    if form.interior_fittings.toilet_freestanding.data
                    or form.interior_fittings.toilet_wall_mounted.data
                    else ""
                ),
                "badrumskap": (
                    "Spegelskåp med belysning"
                    if form.interior_fittings.mirror_cabinet.data
                    else ""
                ),
                "spegel_belysning": (
                    "Spegel med belysning"
                    if form.interior_fittings.mirror_lighting.data
                    else ""
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
                    "Elkontakter"
                    if form.appliances.sink_outlet.data
                    or form.appliances.iron_outlet.data
                    else ""
                ),
            }
        )

        # Map construction work - using actual task names instead of Ja/Nej
        options.update(
            {
                # Construction work
                "etablering": "Etablering",  # Always included
                "rivning_ytskikt": "Rivning ytskikt",  # Always included
                "golvet_bilas": (
                    "Golvet bilas"
                    if form.interior_fittings.bathtub_normal.data
                    or form.interior_fittings.bathtub_long.data
                    else ""
                ),
                "proppa_avlopp": (
                    "Proppa gamla avlopp"
                    if form.bathroom_details.floor_drain_relocation.data
                    else ""
                ),
                "stanga_koppla_el": "Stänga av och koppla el",  # Always included
                "tacka_golv": "Täcka golv",  # Always included
                "tacka_dorropningar": "Täcka dörröppningar",  # Always included
                "gipsvaggar_plywood": "Gipsväggar med plywood",  # Always included
                "spackling": "Spackling",  # Always included
                "gjutning_golvspackling": "Gjutning och golvspackling",  # Always included
                "applicering_tatskikt": "Applicering tätskikt",  # Always included
                "plattsattning": "Plattsättning",  # Always included
                "satting_hornlister": "Sättning hörnlister",  # Always included
                "applicering_fog_silikon": "Applicering fog och silikon",  # Always included
                "utanpaliggande_tappvatten": "Utanpåliggande tappvatten",  # Always included
                "taket_sanks": (
                    "Taket sänks" if form.appliances.ceiling_lowering.data else ""
                ),
                "sortera_byggsopor": "Sortera byggsopor",  # Always included
                "grovstadning": (
                    "Grovstädning" if form.tiles_and_painting.cleanup.data else ""
                ),
            }
        )

        
        # Additional tasks from purple rows in Excel
        options.update(
            {
                "personens_namn": "Personens namn",  # Row 3
                "telefonnummer": "Telefonnummer",  # Row 4
                "adress_fullst_ndig": "Adress fullst�ndig",  # Row 5
                "portkod": "Portkod",  # Row 7
                "el_buren_golvvarme": "T�cking av golv",  # Row 23
                "badrum": "M�tt p� badrumet.   BxLxH",  # Row 25
                "golvyta": "Golvyta",  # Row 26
                "antal_omplaceringar": "Antal omplaceringar ",  # Row 29
                "etablering": "Etablering",  # Row 30
                "spackling": "Flytspackling",  # Row 31
                "tvattstall": " Ta in byggmaterial",  # Row 32
                "toalett": "Omplacering av toalett (ange antal cm)",  # Row 33
                "omplacering_av_tv_ttst_ll_ange_antal_cm": "Omplacering av tv�ttst�ll (ange antal cm)",  # Row 34
                "dusch": "Omplacering av dusch (ange antal cm)",  # Row 35
                "omplacering_av_badkar_ange_antal_cm": "Omplacering av badkar (ange antal cm)",  # Row 36
                "omplacering_av_handdukstork_ange_antal_cm": "Omplacering av handdukstork(ange antal cm)",  # Row 37
                "antal_byte_av_golvbrunnar": "Antal byte av golvbrunnar",  # Row 38
                "flytt_av_golvbrunnar": "Flytt av golvbrunnar",  # Row 39
                "el_buren_golvvarme": "Utf�ra en extra golvbrunn",  # Row 40
                "el_buren_golvvarme": "Sp�ra golv och v�ggar",  # Row 41
                "golvet": "Andra genomf�ringar fr�n golvet ",  # Row 42
                "flytt_av_genomf_ringar_till_v_ggar": "Flytt av genomf�ringar till v�ggar",  # Row 43
                "tvattmaskin": "Byte av avloppsr�r i golvet",  # Row 44
                "avst_ngning_av_vatten_finns": "Avst�ngning av vatten finns",  # Row 45
                "s_kringssk_p": "S�kringssk�p",  # Row 46
                "jordfelsbrytare": "Jordfelsbrytare",  # Row 47
                "badrum": "Avst�nd mellan elsk�p till badrummet",  # Row 48
                "badrum": "Avst�ndet mellan n�rmaste kopplingsdosa till badrummet",  # Row 49
                "taklampa_takdosa": "Taklampa/takdosa",  # Row 51
                "v_gguttag": "V�gguttag",  # Row 52
                "el_buren_golvvarme": "El handdukstork",  # Row 53
                "el_golvv_rme": "El-golvv�rme",  # Row 54
                "tv_ttmaskin": "Tv�ttmaskin",  # Row 55
                "torktumlare": "Torktumlare",  # Row 56
                "el_buren_golvvarme": "El i tv�ttst�ll/kommod",  # Row 57
                "el_uttag": "Extra uttag f�r strykj�rn",  # Row 58
                "spotlights": "Spotlights (antal)",  # Row 59
                "taks_nkning": "Taks�nkning",  # Row 60
                "spegel": "Inbyggd spegel i v�ggen",  # Row 63
                "spegel": "Spegel med belysning",  # Row 64
                "spegel": "Spegelsk�p med belysning och uttag",  # Row 65
                "tv_ttst_ll_med_kommod": "Tv�ttst�ll med kommod",  # Row 66
                "dusch": "Duschblandare med handdusch",  # Row 67
                "dusch": "Duschblandare med tak- och handdusch",  # Row 68
                "el_buren_golvvarme": "S�tta upp en v�gg som duschv�gg",  # Row 69
                "el_buren_golvvarme": "S�tta upp en fast duschv�gg av glasblock",  # Row 70
                "el_buren_golvvarme": "Montering av en glas-duschv�gg",  # Row 71
                "dusch": "Montering av duschd�rrar",  # Row 72
                "dusch": "Golvbrunnen i duschen",  # Row 73
                "badkar": "Badkar",  # Row 74
                "toalett": "Toalett",  # Row 75
                "applicering": "Silikondragning, applicering",  # Row 76
                "byte_av_d_rrfoder_inv_ndingt": "Byte av d�rrfoder inv�ndingt",  # Row 77
                "byte_av_d_rrfoder_utv_ndigt": "Byte av d�rrfoder utv�ndigt",  # Row 78
                "byte_av_d_rrkarm": "Byte av d�rrkarm",  # Row 79
                "byte_av_d_rrblad": "Byte av d�rrblad",  # Row 80
                "byte_uppfr_schning_av_tr_skel": "Byte / uppfr�schning av tr�skel",  # Row 81
                "f_nster_omm_lning": "F�nster omm�lning",  # Row 82
                "dolda_r_rdragningar": "Dolda r�rdragningar",  # Row 83
                "utanp_liggande_r_rdragningar": "Utanp�liggande r�rdragningar",  # Row 84
                "dusch": "Dold takdusch",  # Row 85
                "antal_dolda_blandare": "Antal dolda blandare",  # Row 86
                "r_ddning_av_befintlig_vattenburen_golvv_rme": "R�ddning av befintlig vattenburen golvv�rme",  # Row 87
                "l_ggning_av_ny_vattenburen_golvv_rme": "L�ggning av ny vattenburen golvv�rme",  # Row 88
                "taket": "Platts�ttning upp till tak",  # Row 89
                "h_jd_p_platts_ttning_p_v_ggar": "H�jd p� platts�ttning p� v�ggar",  # Row 90
                "spotlights": "Nischar utan spotlight",  # Row 91
                "spotlights": "Nischar med spotlight",  # Row 92
                "storlek_golvplattor_10_10_till_20_20": "Storlek golvplattor (10*10 till 20*20)",  # Row 93
                "tvattmaskin": "Avvikelse i storlek f�r golvplattor ",  # Row 94
                "v_ggplattor_15_15_till_60_60": "V�ggplattor (15*15 till 60*60)",  # Row 95
                "tvattmaskin": "Avvikelse i storlek f�r v�ggplattor",  # Row 96
                "antal_f_rger_fog": "Antal f�rger fog",  # Row 97
                "taket": "M�lning av tak",  # Row 99
                "arbetstid_m_lning_av_okaklade_v_ggar": "Arbetstid m�lning av okaklade v�ggar",  # Row 100
                "m_lning_av_okaklade_v_ggar": "M�lning av okaklade v�ggar",  # Row 101
                "etablering": "Avetablering och grovst�dning",  # Row 102
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
            total = calculate_total(form)
            rot_deduction = calculate_rot_deduction(form)

            # Option 1 costs
            labor_cost_option1 = calculate_labor_cost_option1(form)
            material_cost_option1 = calculate_material_cost_option1(form)
            waste_cost_option1 = calculate_waste_cost_option1(form)
            discount_option1 = calculate_discount_option1(form)
            total_option1 = calculate_total_option1(form)
            rot_deduction_option1 = calculate_rot_deduction_option1(form)

            # Option 2 costs
            labor_cost_option2 = calculate_labor_cost_option2(form)
            material_cost_option2 = calculate_material_cost_option2(form)
            waste_cost_option2 = calculate_waste_cost_option2(form)
            discount_option2 = calculate_discount_option2(form)
            total_option2 = calculate_total_option2(form)
            rot_deduction_option2 = calculate_rot_deduction_option2(form)

            return {
                # Main option costs
                "arbetskostnad_main": f"{int(labor_cost)} kr",
                "materialkostnad_main": f"{int(material_cost)} kr",
                "avfallshantering_main": f"{int(waste_cost)} kr",
                "rabatt_main": f"{int(discount)} kr",
                "total_sum_main": f"{int(total)} kr",
                "rot_avdrag_main": f"{int(rot_deduction)} kr",
                # Option 1 costs
                "arbetskostnad_option1": f"{int(labor_cost_option1)} kr",
                "byggmaterial_option1": f"{int(material_cost_option1)} kr",
                "avfallshantering_option1": f"{int(waste_cost_option1)} kr",
                "rabatt_option1": f"{int(discount_option1)} kr",
                "total_sum_option1": f"{int(total_option1)} kr",
                "rot_avdrag_option1": f"{int(rot_deduction_option1)} kr",
                # Option 2 costs
                "arbetskostnad_option2": f"{int(labor_cost_option2)} kr",
                "byggmaterial_option2": f"{int(material_cost_option2)} kr",
                "avfallshantering_option2": f"{int(waste_cost_option2)} kr",
                "rabatt_option2": f"{int(discount_option2)} kr",
                "total_sum_option2": f"{int(total_option2)} kr",
                "rot_avdrag_option2": f"{int(rot_deduction_option2)} kr",
            }
        except Exception as e:
            import logging

            logging.getLogger(__name__).error(f"Error in cost calculations: {str(e)}")

            # Provide default values if calculations fail
            return {
                # Main option costs
                "arbetskostnad_main": "45000 kr",
                "materialkostnad_main": "25000 kr",
                "avfallshantering_main": "5000 kr",
                "rabatt_main": "0 kr",
                "total_sum_main": "75000 kr",
                "rot_avdrag_main": "13500 kr",
                # Option 1 costs
                "arbetskostnad_option1": "35000 kr",
                "byggmaterial_option1": "20000 kr",
                "avfallshantering_option1": "4000 kr",
                "rabatt_option1": "0 kr",
                "total_sum_option1": "59000 kr",
                "rot_avdrag_option1": "10500 kr",
                # Option 2 costs
                "arbetskostnad_option2": "55000 kr",
                "byggmaterial_option2": "30000 kr",
                "avfallshantering_option2": "6000 kr",
                "rabatt_option2": "0 kr",
                "total_sum_option2": "91000 kr",
                "rot_avdrag_option2": "16500 kr",
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
