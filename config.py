




show_time = False

gen_time = 0
gen_start = 0
max_gen_time = 30


current_life = 0

dead_start = 0
dead_time = 0

alive_start = 0
alive_time = 0


alive_array = []

PERKS = {
	"Coordinated" : 600,
	"Overkill" : 20,

	"Resourceful" : 10,

	"Artisanistry" : 30,
	"Siphonology" : 5,

	"HEALTH" : 40,
	"ATTACK" : 70,
	"LOOTING" : 80,
	"CARPENTRY" : 200,
	"MOTIVATION" : 40,

	"Agility" : 1,
	
	"Anticipation" : 1,
	
	"Bait" : 1,
	"Pheromones": 1,
	
	"Relentlessness" : 1,
	"Meditation" : 1,
	"Trumps": 1,
	"Range" : 1,
	"Packrat" : 1,
}

PERK_GROUP = {
	"HEALTH" : ["Toughness", "Toughness_II", "Resilience"],
	"ATTACK" : ["Power", "Power_II"],
	"LOOTING" : ["Looting", "Looting_II"],
	"CARPENTRY" : ["Carpentry", "Carpentry_II"],
	"MOTIVATION" : ["Motivation", "Motivation_II"],
}

current_challenge = "none"
SCRYING_FORMATION = 275

CHALLENGES = {
	"none" : {
		"void_maps_at" : 270,
		"gigastation_preset" : (120, 3 ),
		"portal_at" : 271,
		"geneticist_target" : 3,
	},
	"Nom" : {
		"void_maps_at" : 145,
		"gigastation_preset" : (8, 4),
		"portal_at" : 146,
		"geneticist_target" : 30,
	},
	"Toxicity" : {
		"void_maps_at" : 165, # 33
		"gigastation_preset" : (33, 3),
		"portal_at" : 168,
		"geneticist_tar72get" : 3,
	},
	"Corrupted" : {
		"void_maps_at" : 190, # 33
		"gigastation_preset" : (65, 3),
		"portal_at" : 191,
		"geneticist_target" : 3,
	},
	"Domination" : {
		"void_maps_at" : 215, # 33
		"gigastation_preset" : (90, 3),
		"portal_at" : 216,
		"geneticist_target" : 30,
	},
	
}