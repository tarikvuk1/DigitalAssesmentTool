import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    new_columns = []

    for col in df.columns:
        col_clean = (
            str(col)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("?", "")
            .replace("/", "_")
            .replace("(", "")
            .replace(")", "")
            .replace(",", "")
            .replace(".", "")
            .replace("-", "_")
        )

        new_columns.append(col_clean)

    df.columns = new_columns
    df = df.loc[:, ~df.columns.str.startswith("unnamed")]
    return df


def rename_key_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    rename_map = {
        "naziv_kompanije": "company_name",
        "id_broj": "company_id",
        "email": "email",
        "kojoj_industriji_pripada_kompanija": "industry",
        "gdje_je_lokacija_kompanije": "location",
        "da_li_imate_interno_it_odjeljenje_ili_koristite_usluge_drugih_kompanija_za_svoje_it_potrebe": "it_support",
        "da_li_planirate_da_investirate_u_digitalne_projekte": "digital_investment_plan",
        "koji_softver_koristite": "software_used",
        "da_li_vaši_zaposleni_na_personalnom_kompjuteru_ili_sličnim_uređajima_koriste_ili_imaju_pristup_internetu": "internet_access",
        "da_li_koristite_elektronsku_poštu_da_li_imate_elektronsku_poštu_na_domenu_vaše_kompanije_na_primjer_imeprezimekompanijaba": "business_email",
        "da_li_u_okviru_vaše_kompanije_koristite_alate_za_zajednički_rad_google_drive_one_drive_i_čuvanje_kako_bi_se_svi_relevantni_dokumenti_nalazili_na_jednom_mjestu_za_sve_uključene_u_proces": "collaboration_tools",
        "da_li_ste_pretraživali_internet_zbog_novih_dobavljača_za_proizvode_i_usluge_u_posljednje_2_godine_ili_da_li_ste_se_kvalifikovali_za_online_dobavljača": "search_suppliers_online",
        "da_li_od_vaših_glavnih_dobavljača_poručujete_elektronski_ne_faksom": "electronic_ordering",
        "da_li_bar_neke_fakture_primate_elektronski": "receive_e_invoices",
        "da_li_elektronski_obrađujete_elektronske_fakture_u_vašem_sopstvenom_sistemu_upravljanja_preduzećem_na_primjer_erp_itd": "process_e_invoices",
        "da_li_se_podaci_u_lancu_procesa_od_prodaje_preko_proizvodnje_do_administracije_i_obrnuto_prenose_elektronski_u_vašem_sopstvenom_sistemu_upravljanja_preduzećem_na_primjer_erp_itd": "digital_data_flow",
        "da_li_koristite_online_alate_platforme_itd_prilikom_angažovanja_novih_radnika": "digital_recruitment",
        "kako_upravljate_kadrovskom_administracijom_na_primjer_godišnji_odmori_platni_spiskovi_ili_prekovremeni_rad": "hr_admin",
        "da_li_koristite_sljedeće_elektronske_alate_za_obuku_ili_dalje_usavršavanje_zaposlenih_molimo_vas_da_odaberete_sve_primjenjive_odgovore": "digital_training_tools",
        "kako_vidite_digitalne_vještine_u_vašoj_kompaniji": "digital_skills",
        "da_li_imate_web_site": "has_website",
        "da_li_pratite___radite_na_onlajn_reputaciji_vaše_kompanije_i_na_prometu_na_web_site_u_na_primjer_rezultati_pretrage_na_google_teme_foruma_razgovori_na_facebooku_u_twitteru": "online_reputation",
        "da_li_se_bavite_praćenjem_ponašanja_korisnika_na_vašem_web_site_u_zarad_veće_prodaje_i_boljeg_razumijevanja_potrošača_google_analitika_matomo_facebook_piksel_hotjar_itd": "website_analytics",
        "da_li_pratite_podatke_o_potrošnji_kupovini_individualnih_klijenata_i_da_li_imate_razrađenu_šemu_lojalnosti_za_najvjernije_mušterije": "customer_loyalty",
        "da_li_ste_ikada_vodili_kampanju_na_društvenim_medijima_koja_je_trajala_najmanje_šest_mjeseci": "social_media_campaigns",
        "da_li_ste_se_ikada_bavili_segmentacijom_kupaca_na_osnovu_podataka_koje_ste_generisali_na_društvenim_mrežama": "customer_segmentation",
        "da_li_imate_internog_menadžera_za_društvene_medije_ili_koristite_usluge_drugih_kompanija_za_svoje_potrebe": "social_media_management",
        "koje_mjere_za_it_bezbjednost_ste_uspostavili_molimo_vas_da_odaberete_sve_primjenjive_odgovore": "it_security_measures",
    }

    existing_map = {k: v for k, v in rename_map.items() if k in df.columns}
    df = df.rename(columns=existing_map)

    return df


def map_yes_no(value):
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    if value in ["da", "yes"]:
        return 1
    elif value in ["ne", "no"]:
        return 0
    else:
        return None