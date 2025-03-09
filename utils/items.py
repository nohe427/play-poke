def generate_constants():
    """Generates a dictionary of constants from the provided ASM-like definitions."""

    constants = {}
    const_value = 1

    items_and_badges = [
        "MASTER_BALL", "ULTRA_BALL", "GREAT_BALL", "POKE_BALL", "TOWN_MAP", "BICYCLE", "SURFBOARD",
        "SAFARI_BALL", "POKEDEX", "MOON_STONE", "ANTIDOTE", "BURN_HEAL", "ICE_HEAL", "AWAKENING",
        "PARLYZ_HEAL", "FULL_RESTORE", "MAX_POTION", "HYPER_POTION", "SUPER_POTION", "POTION",
        "BOULDERBADGE", "CASCADEBADGE", "THUNDERBADGE", "RAINBOWBADGE", "SOULBADGE", "MARSHBADGE",
        "VOLCANOBADGE", "EARTHBADGE", "ESCAPE_ROPE", "REPEL", "OLD_AMBER", "FIRE_STONE",
        "THUNDER_STONE", "WATER_STONE", "HP_UP", "PROTEIN", "IRON", "CARBOS", "CALCIUM",
        "RARE_CANDY", "DOME_FOSSIL", "HELIX_FOSSIL", "SECRET_KEY", "UNUSED_ITEM", "BIKE_VOUCHER",
        "X_ACCURACY", "LEAF_STONE", "CARD_KEY", "NUGGET", "PP_UP_2", "POKE_DOLL", "FULL_HEAL",
        "REVIVE", "MAX_REVIVE", "GUARD_SPEC", "SUPER_REPEL", "MAX_REPEL", "DIRE_HIT", "COIN",
        "FRESH_WATER", "SODA_POP", "LEMONADE", "S_S_TICKET", "GOLD_TEETH", "X_ATTACK", "X_DEFEND",
        "X_SPEED", "X_SPECIAL", "COIN_CASE", "OAKS_PARCEL", "ITEMFINDER", "SILPH_SCOPE",
        "POKE_FLUTE", "LIFT_KEY", "EXP_ALL", "OLD_ROD", "GOOD_ROD", "SUPER_ROD", "PP_UP", "ETHER",
        "MAX_ETHER", "ELIXER", "MAX_ELIXER", "FLOOR_B2F", "FLOOR_B1F", "FLOOR_1F", "FLOOR_2F",
        "FLOOR_3F", "FLOOR_4F", "FLOOR_5F", "FLOOR_6F", "FLOOR_7F", "FLOOR_8F", "FLOOR_9F",
        "FLOOR_10F", "FLOOR_11F", "FLOOR_B4F"
    ]

    for item in items_and_badges:
        constants[const_value] = item
        const_value += 1

    # Overloads
    constants["SAFARI_BAIT"] = 0x15
    constants["SAFARI_ROCK"] = 0x16

    const_value = 0xC4

    hms_and_tms = [
        "HM_01", "HM_02", "HM_03", "HM_04", "HM_05", "TM_01", "TM_02", "TM_03", "TM_04", "TM_05",
        "TM_06", "TM_07", "TM_08", "TM_09", "TM_10", "TM_11", "TM_12", "TM_13", "TM_14", "TM_15",
        "TM_16", "TM_17", "TM_18", "TM_19", "TM_20", "TM_21", "TM_22", "TM_23", "TM_24", "TM_25",
        "TM_26", "TM_27", "TM_28", "TM_29", "TM_30", "TM_31", "TM_32", "TM_33", "TM_34", "TM_35",
        "TM_36", "TM_37", "TM_38", "TM_39", "TM_40", "TM_41", "TM_42", "TM_43", "TM_44", "TM_45",
        "TM_46", "TM_47", "TM_48", "TM_49", "TM_50"
    ]

    for item in hms_and_tms:
        constants[const_value] = item
        const_value += 1

    return constants

# Example usage:
# constants = generate_constants()
# print(constants)

# # Example of how to access a constant:
# print(f"POKE_BALL: {constants[4]}")
# # print(f"TM_01: {constants['TM_01']}")