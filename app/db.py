from datetime import datetime, timezone

from .models import (
    db,
    RegisteredUser,
    Quiz,
    QuizResult,
)


def find_registered_user_by_identifier(identifier):
    return RegisteredUser.query.filter(
        (RegisteredUser.username == identifier) | (RegisteredUser.email == identifier)
    ).first()


def save_registered_user(
    first_name, last_name, email, username, password_hash, terms_read
):
    user = RegisteredUser(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password_hash=password_hash,
        terms_read=terms_read == "yes",
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(user)
    db.session.commit()


def get_all_quizzes():
    return Quiz.query.all()


def _make_question(question, correct, wrong_options, index):
    """Create one Quiz-compatible dictionary and rotate the correct answer letter."""
    clean_wrong_options = []
    for option in wrong_options:
        if option != correct and option not in clean_wrong_options:
            clean_wrong_options.append(option)

    options = clean_wrong_options[:3]
    insert_at = index % 4
    options.insert(insert_at, correct)

    correct_answer = "ABCD"[insert_at]
    return {
        "question": question,
        "selection_a": options[0],
        "selection_b": options[1],
        "selection_c": options[2],
        "selection_d": options[3],
        "correct_answer": correct_answer,
    }


def _make_science_questions():
    questions = []

    element_symbols = [
        ("hydrogen", "H"),
        ("helium", "He"),
        ("carbon", "C"),
        ("oxygen", "O"),
        ("nitrogen", "N"),
        ("sodium", "Na"),
        ("potassium", "K"),
        ("iron", "Fe"),
        ("copper", "Cu"),
        ("silver", "Ag"),
        ("gold", "Au"),
        ("mercury", "Hg"),
        ("lead", "Pb"),
        ("tin", "Sn"),
        ("chlorine", "Cl"),
        ("calcium", "Ca"),
        ("magnesium", "Mg"),
        ("aluminium", "Al"),
        ("silicon", "Si"),
        ("sulfur", "S"),
    ]
    symbol_wrongs = [
        "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
        "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
        "Fe", "Cu", "Zn", "Ag", "Sn", "Au", "Hg", "Pb",
    ]
    for element, symbol in element_symbols:
        questions.append((f"What is the chemical symbol for {element}?", symbol, symbol_wrongs))

    si_units = [
        ("force", "newton"),
        ("energy", "joule"),
        ("power", "watt"),
        ("electric current", "ampere"),
        ("voltage", "volt"),
        ("electrical resistance", "ohm"),
        ("frequency", "hertz"),
        ("pressure", "pascal"),
        ("temperature", "kelvin"),
        ("electric charge", "coulomb"),
        ("magnetic flux density", "tesla"),
        ("luminous intensity", "candela"),
    ]
    unit_wrongs = [unit for _, unit in si_units]
    for quantity, unit in si_units:
        questions.append((f"What is the SI unit of {quantity}?", unit, unit_wrongs))

    science_facts = [
        ("Which planet is known as the Red Planet?", "Mars", ["Venus", "Jupiter", "Saturn", "Mercury"]),
        ("Which planet is closest to the Sun?", "Mercury", ["Venus", "Earth", "Mars", "Neptune"]),
        ("Which planet is the largest in the solar system?", "Jupiter", ["Earth", "Saturn", "Uranus", "Neptune"]),
        ("Which planet is famous for its large ring system?", "Saturn", ["Mars", "Jupiter", "Venus", "Mercury"]),
        ("What is Earth&apos;s natural satellite?", "The Moon", ["Mars", "Titan", "Europa", "Venus"]),
        ("What gas do plants absorb during photosynthesis?", "Carbon dioxide", ["Oxygen", "Nitrogen", "Hydrogen", "Helium"]),
        ("What gas do humans need for respiration?", "Oxygen", ["Carbon dioxide", "Nitrogen", "Argon", "Methane"]),
        ("What is the most abundant gas in Earth&apos;s atmosphere?", "Nitrogen", ["Oxygen", "Carbon dioxide", "Argon", "Hydrogen"]),
        ("What is the pH of pure water at room temperature?", "7", ["0", "4", "10", "14"]),
        ("What is the chemical formula for water?", "H2O", ["CO2", "O2", "NaCl", "CH4"]),
        ("What is the chemical formula for carbon dioxide?", "CO2", ["H2O", "O2", "NaCl", "NH3"]),
        ("Which state of matter has a fixed shape and fixed volume?", "Solid", ["Liquid", "Gas", "Plasma", "Vapour"]),
        ("Which state of matter has fixed volume but no fixed shape?", "Liquid", ["Solid", "Gas", "Plasma", "Crystal"]),
        ("Which process changes a liquid into a gas at the surface?", "Evaporation", ["Freezing", "Condensation", "Melting", "Deposition"]),
        ("Which process changes a gas into a liquid?", "Condensation", ["Evaporation", "Sublimation", "Melting", "Freezing"]),
        ("Which subatomic particle has a negative charge?", "Electron", ["Proton", "Neutron", "Nucleus", "Ion"]),
        ("Which subatomic particle has a positive charge?", "Proton", ["Electron", "Neutron", "Photon", "Atom"]),
        ("Which subatomic particle has no electric charge?", "Neutron", ["Electron", "Proton", "Ion", "Molecule"]),
        ("What is the centre of an atom called?", "Nucleus", ["Electron cloud", "Molecule", "Ion", "Cell"]),
        ("What is a substance with pH less than 7 called?", "Acid", ["Base", "Salt", "Solvent", "Metal"]),
        ("What is a substance with pH greater than 7 called?", "Base", ["Acid", "Salt", "Isotope", "Mineral"]),
        ("What is formed when two or more elements chemically combine?", "Compound", ["Mixture", "Solution", "Atom", "Alloy only"]),
        ("Which force pulls objects toward Earth?", "Gravity", ["Friction", "Magnetism", "Electricity", "Buoyancy"]),
        ("What type of energy is stored in a stretched rubber band?", "Potential energy", ["Kinetic energy", "Thermal energy", "Sound energy", "Light energy"]),
        ("What is the approximate speed of light in a vacuum?", "300,000 km/s", ["150,000 km/s", "450,000 km/s", "600,000 km/s", "30,000 km/s"]),
        ("Which scientist developed the theory of relativity?", "Albert Einstein", ["Isaac Newton", "Galileo Galilei", "Marie Curie", "Charles Darwin"]),
        ("Who is known for the laws of motion and universal gravitation?", "Isaac Newton", ["Albert Einstein", "Nikola Tesla", "Niels Bohr", "Gregor Mendel"]),
        ("Which layer of Earth lies directly below the crust?", "Mantle", ["Outer core", "Inner core", "Atmosphere", "Lithosphere only"]),
        ("What instrument measures earthquakes?", "Seismograph", ["Barometer", "Thermometer", "Hygrometer", "Anemometer"]),
        ("Which type of rock forms from cooled magma or lava?", "Igneous", ["Sedimentary", "Metamorphic", "Fossil", "Mineral"]),
        ("Which type of rock forms from layers of sediment?", "Sedimentary", ["Igneous", "Metamorphic", "Basalt", "Granite"]),
        ("What is the process of wearing away rocks and soil called?", "Erosion", ["Condensation", "Combustion", "Photosynthesis", "Freezing"]),
        ("What causes ocean tides on Earth?", "The Moon&apos;s gravity", ["Earthquakes", "Volcanoes", "Wind only", "Lightning"]),
        ("Which electromagnetic waves have the shortest wavelength?", "Gamma rays", ["Radio waves", "Microwaves", "Visible light", "Infrared"]),
        ("Which colour of visible light has the longest wavelength?", "Red", ["Violet", "Blue", "Green", "Yellow"]),
        ("What kind of mirror curves inward?", "Concave mirror", ["Convex mirror", "Plane mirror", "Transparent mirror", "Flat mirror"]),
        ("Which simple machine is a ramp?", "Inclined plane", ["Lever", "Pulley", "Wheel and axle", "Screwdriver"]),
        ("What is the freezing point of water at standard pressure?", "0°C", ["50°C", "100°C", "-100°C", "25°C"]),
        ("What is the boiling point of water at standard pressure?", "100°C", ["0°C", "50°C", "200°C", "25°C"]),
        ("What is the name for the path of a planet around the Sun?", "Orbit", ["Axis", "Crater", "Tide", "Equator"]),
        ("What is one complete turn of Earth on its axis called?", "Rotation", ["Revolution", "Orbit", "Eclipse", "Solstice"]),
        ("What is one complete trip of Earth around the Sun called?", "Revolution", ["Rotation", "Eclipse", "Tide", "Axis"]),
        ("Which event occurs when the Moon blocks the Sun from view?", "Solar eclipse", ["Lunar eclipse", "Solstice", "Equinox", "Comet"]),
        ("Which event occurs when Earth&apos;s shadow falls on the Moon?", "Lunar eclipse", ["Solar eclipse", "Solstice", "Meteor shower", "Tide"]),
        ("What is the hardest natural mineral?", "Diamond", ["Quartz", "Talc", "Calcite", "Gypsum"]),
        ("What instrument measures air pressure?", "Barometer", ["Thermometer", "Anemometer", "Rain gauge", "Compass"]),
        ("What instrument measures wind speed?", "Anemometer", ["Barometer", "Thermometer", "Compass", "Seismograph"]),
        ("Which branch of science studies living things?", "Biology", ["Physics", "Chemistry", "Geology", "Astronomy"]),
        ("Which branch of science studies matter and its changes?", "Chemistry", ["Physics", "Biology", "Astronomy", "Ecology"]),
        ("Which branch of science studies forces and energy?", "Physics", ["Chemistry", "Biology", "Botany", "Zoology"]),
        ("Which gas in the atmosphere helps block ultraviolet radiation?", "Ozone", ["Hydrogen", "Methane", "Helium", "Nitrogen"]),
        ("What is the main source of energy for Earth&apos;s climate system?", "The Sun", ["The Moon", "Earth&apos;s core", "Comets", "Lightning"]),
        ("Which material is a good conductor of electricity?", "Copper", ["Rubber", "Glass", "Plastic", "Wood"]),
        ("Which material is commonly used as an electrical insulator?", "Rubber", ["Copper", "Aluminium", "Silver", "Iron"]),
        ("What is the main gas released when fossil fuels burn completely?", "Carbon dioxide", ["Oxygen", "Helium", "Neon", "Hydrogen"]),
        ("Which process allows heat to travel through direct contact?", "Conduction", ["Convection", "Radiation", "Condensation", "Refraction"]),
        ("Which process transfers heat through moving fluids?", "Convection", ["Conduction", "Radiation", "Reflection", "Diffusion"]),
        ("Which process transfers heat by electromagnetic waves?", "Radiation", ["Conduction", "Convection", "Evaporation", "Sublimation"]),
        ("Which lens is thicker in the middle and converges light?", "Convex lens", ["Concave lens", "Plane mirror", "Prism", "Flat lens"]),
        ("What is the study of weather called?", "Meteorology", ["Geology", "Astronomy", "Ecology", "Botany"]),
        ("What is the study of stars and space called?", "Astronomy", ["Biology", "Chemistry", "Meteorology", "Geology"]),
        ("What is the study of Earth&apos;s rocks and structure called?", "Geology", ["Astronomy", "Zoology", "Botany", "Physics"]),
        ("Which particle of light is called a photon?", "Photon", ["Proton", "Neutron", "Electron", "Ion"]),
        ("Which renewable energy source uses moving air?", "Wind energy", ["Coal energy", "Nuclear energy", "Natural gas", "Diesel energy"]),
        ("Which renewable energy source uses sunlight?", "Solar energy", ["Coal energy", "Petrol energy", "Diesel energy", "Natural gas"]),
        ("Which scientific tool is used to view very small objects?", "Microscope", ["Telescope", "Periscope", "Barometer", "Compass"]),
        ("Which scientific tool is used to view distant objects in space?", "Telescope", ["Microscope", "Thermometer", "Seismograph", "Hygrometer"]),
        ("What is the unit used to measure temperature in most science contexts?", "Kelvin", ["Metre", "Second", "Mole", "Newton"]),
    ]
    questions.extend(science_facts)
    return [_make_question(question, correct, wrongs, index) for index, (question, correct, wrongs) in enumerate(questions[:100])]


def _make_programming_questions():
    questions = []

    acronyms = [
        ("HTML", "Hyper Text Markup Language"),
        ("CSS", "Cascading Style Sheets"),
        ("SQL", "Structured Query Language"),
        ("API", "Application Programming Interface"),
        ("URL", "Uniform Resource Locator"),
        ("HTTP", "Hypertext Transfer Protocol"),
        ("HTTPS", "Hypertext Transfer Protocol Secure"),
        ("JSON", "JavaScript Object Notation"),
        ("XML", "Extensible Markup Language"),
        ("DOM", "Document Object Model"),
        ("IDE", "Integrated Development Environment"),
        ("CLI", "Command Line Interface"),
        ("GUI", "Graphical User Interface"),
        ("CPU", "Central Processing Unit"),
        ("RAM", "Random Access Memory"),
        ("OOP", "Object-Oriented Programming"),
        ("CRUD", "Create, Read, Update, Delete"),
        ("DNS", "Domain Name System"),
        ("TCP", "Transmission Control Protocol"),
        ("IP", "Internet Protocol"),
    ]
    acronym_wrongs = ["Central Runtime Unit", "Common Resource Data", "Computer Render Format", "Control Response Device"]
    for acronym, answer in acronyms:
        questions.append((f"What does {acronym} stand for?", answer, acronym_wrongs))

    programming_facts = [
        ("Which keyword is used to define a function in Python?", "def", ["function", "func", "define", "method"]),
        ("Which symbol starts a single-line comment in Python?", "#", ["//", "<!--", "/*", "--"]),
        ("Which Python data type stores key-value pairs?", "dictionary", ["list", "tuple", "string", "integer"]),
        ("Which Python data type is immutable?", "tuple", ["list", "dictionary", "set", "bytearray"]),
        ("Which Python keyword starts a conditional statement?", "if", ["for", "try", "with", "return"]),
        ("Which Python keyword handles exceptions?", "except", ["catch", "error", "handle", "rescue"]),
        ("Which Python keyword creates a loop over a sequence?", "for", ["def", "class", "return", "import"]),
        ("Which Python value represents no value?", "None", ["null", "nil", "zero", "empty"]),
        ("Which Python function returns the length of a sequence?", "len()", ["size()", "length()", "count()", "total()"]),
        ("Which operator tests equality in many programming languages?", "==", ["=", "!=", "<=", ">="]),
        ("Which operator is commonly used for assignment?", "=", ["==", "!=", "=>", "<="]),
        ("Which data structure uses LIFO order?", "Stack", ["Queue", "Array", "Tree", "Graph"]),
        ("Which data structure uses FIFO order?", "Queue", ["Stack", "Graph", "Set", "Tree"]),
        ("Which data structure represents hierarchical data?", "Tree", ["Queue", "Stack", "Array", "String"]),
        ("Which data structure represents nodes connected by edges?", "Graph", ["Stack", "Queue", "String", "Tuple"]),
        ("Which structure stores unique unordered values in Python?", "set", ["list", "tuple", "str", "dict values only"]),
        ("What is a linked list made of?", "Nodes", ["Pixels", "Rows only", "Packets only", "Tables"]),
        ("What is recursion?", "A function calling itself", ["A database table", "A network protocol", "A style sheet", "A hardware cable"]),
        ("What is an algorithm?", "Step-by-step solution", ["Computer brand", "File icon", "Login screen", "Monitor type"]),
        ("What is Big O notation used for?", "Describing algorithm efficiency", ["Designing fonts", "Naming variables", "Encrypting files", "Choosing colours"]),
        ("What is O(1) complexity called?", "Constant time", ["Linear time", "Quadratic time", "Exponential time", "Factorial time"]),
        ("What is O(n) complexity called?", "Linear time", ["Constant time", "Logarithmic time", "Quadratic time", "Cubic time"]),
        ("What is the average time complexity of binary search?", "O(log n)", ["O(n)", "O(n^2)", "O(1)", "O(n!)"]),
        ("Which search checks items one by one?", "Linear search", ["Binary search", "Hash search", "Merge search", "Tree rotation"]),
        ("Which sorting algorithm repeatedly compares adjacent items?", "Bubble sort", ["Binary search", "Dijkstra&apos;s algorithm", "Depth-first search", "Breadth-first search"]),
        ("Which algorithm finds the shortest path in a weighted graph?", "Dijkstra&apos;s algorithm", ["Bubble sort", "Linear search", "Insertion sort", "Selection sort"]),
        ("What does a compiler do?", "Translates source code", ["Stores images", "Designs icons", "Routes emails", "Measures voltage"]),
        ("What does an interpreter do?", "Executes code line by line", ["Creates hardware", "Deletes databases", "Draws circuits", "Builds monitors"]),
        ("What is debugging?", "Finding and fixing errors", ["Writing marketing copy", "Compressing images only", "Buying software", "Designing logos"]),
        ("What is a syntax error?", "Code grammar mistake", ["Wrong password", "Slow internet", "Missing monitor", "Power failure"]),
        ("What is a runtime error?", "An error while the program runs", ["A design colour", "A type of cable", "A spreadsheet formula", "A file extension"]),
        ("What is a variable?", "A named storage location", ["A fixed hardware chip", "A monitor type", "A network cable", "A printer"]),
        ("What is a Boolean value?", "True or false", ["Whole number only", "Text string only", "File path", "Image file"]),
        ("What is a class in object-oriented programming?", "A blueprint for objects", ["A CPU register", "A web address", "A database backup", "A comment block"]),
        ("What is an object in object-oriented programming?", "An instance of a class", ["A file extension", "A loop counter only", "A router", "A cable"]),
        ("Which OOP concept hides internal details?", "Encapsulation", ["Inheritance", "Polymorphism", "Compilation", "Indexing"]),
        ("Which OOP concept lets a class reuse features from another class?", "Inheritance", ["Looping", "Indexing", "Parsing", "Hashing"]),
        ("Which OOP concept allows one interface to have many forms?", "Polymorphism", ["Caching", "Sorting", "Hashing", "Tokenising"]),
        ("Which SQL command retrieves data?", "SELECT", ["INSERT", "UPDATE", "DELETE", "DROP"]),
        ("Which SQL command adds a new record?", "INSERT", ["SELECT", "UPDATE", "DROP", "ALTER"]),
        ("Which SQL command changes existing records?", "UPDATE", ["SELECT", "INSERT", "CREATE", "JOIN"]),
        ("Which SQL command removes records?", "DELETE", ["JOIN", "ORDER", "WHERE", "GROUP"]),
        ("Which SQL clause filters rows?", "WHERE", ["FROM", "GROUP BY", "ORDER BY", "SELECT"]),
        ("Which SQL clause sorts query results?", "ORDER BY", ["WHERE", "JOIN", "HAVING", "INSERT"]),
        ("What is a primary key?", "Unique row identifier", ["CSS selector", "Network packet", "Loop variable", "Font family"]),
        ("What is a foreign key?", "A link to a key in another table", ["Password hint", "Browser extension", "Hidden file", "Operating system"]),
        ("Which HTML tag creates a hyperlink?", "<a>", ["<p>", "<div>", "<img>", "<span>"]),
        ("Which HTML tag displays an image?", "<img>", ["<link>", "<script>", "<style>", "<section>"]),
        ("Which HTML tag is used for the largest heading?", "<h1>", ["<h6>", "<head>", "<header>", "<p>"]),
        ("What does CSS selector .menu target?", "Elements with class menu", ["Element with id menu", "All menu tags only", "The body element", "All images"]),
        ("What does CSS selector #main target?", "Element with id main", ["Elements with class main", "All paragraphs", "All links", "All headings"]),
        ("Which HTTP method is commonly used to request data?", "GET", ["POST", "PUT", "DELETE", "PATCH"]),
        ("Which HTTP method is commonly used to submit new data?", "POST", ["GET", "HEAD", "TRACE", "OPTIONS"]),
        ("Which HTTP status code means OK?", "200", ["301", "404", "500", "403"]),
        ("Which HTTP status code means Not Found?", "404", ["200", "301", "500", "201"]),
        ("What is version control used for?", "Tracking changes in files", ["Cooling a CPU", "Drawing diagrams only", "Blocking websites", "Changing monitor brightness"]),
        ("Which Git command saves staged changes to repository history?", "git commit", ["git push", "git pull", "git status", "git init"]),
        ("Which Git command downloads changes from a remote repository?", "git pull", ["git init", "git add", "git log", "git status"]),
        ("Which Git command uploads commits to a remote repository?", "git push", ["git clone", "git diff", "git branch", "git init"]),
        ("What is a repository?", "A project storage location", ["A keyboard shortcut", "A type of loop", "A single variable", "A screen saver"]),
        ("What is a software framework?", "Reusable structure for building software", ["Physical computer case", "Database password", "Binary digit", "Image file"]),
        ("What is a software library?", "Reusable code collection", ["Network address only", "CPU instruction only", "File permission", "Router port"]),
        ("What is unit testing?", "Testing small parts of code", ["Testing only the monitor", "Testing a router cable", "Testing passwords only", "Testing a printer"]),
        ("What does authentication verify?", "A user&apos;s identity", ["A page colour", "A file size", "CPU speed", "Screen resolution"]),
        ("What does authorization decide?", "What an authenticated user may access", ["The spelling of variables", "Monitor brightness", "Number of pixels", "Keyboard layout"]),
        ("What is hashing commonly used for?", "Storing passwords safely", ["Styling text", "Drawing icons", "Counting loops", "Changing font size"]),
        ("What is encryption used for?", "Protecting data by encoding it", ["Sorting arrays", "Changing font size", "Deleting comments", "Counting pixels"]),
        ("Which number system uses only 0 and 1?", "Binary", ["Decimal", "Hexadecimal", "Octal", "Duodecimal"]),
        ("Which file type is commonly used for Python source code?", ".py", [".html", ".css", ".jpg", ".sql"]),
        ("Which command-line command commonly lists files on Unix-like systems?", "ls", ["cd", "mkdir", "pwd", "rm"]),
        ("Which command-line command changes the current directory?", "cd", ["ls", "echo", "cat", "touch"]),
        ("Which command-line command prints the current directory on Unix-like systems?", "pwd", ["mkdir", "cd", "rm", "grep"]),
        ("What is an exception?", "An error condition that can be handled", ["A CSS class", "A database table", "A CPU core", "A screen size"]),
        ("What is pseudocode?", "Informal code-like algorithm description", ["Compiled machine code", "Encrypted password", "Browser cache", "Network cable"]),
        ("What is an infinite loop?", "A loop that never ends by itself", ["A loop that runs once", "A database backup", "A website link", "A colour palette"]),
        ("What is an off-by-one error?", "A boundary counting mistake", ["A missing server", "A broken monitor", "A database index only", "A hardware fault"]),
        ("What is a parameter in a function?", "Input variable for the function", ["Output file only", "Database row", "CSS colour", "Network address"]),
        ("What is a return value?", "The output sent back by a function", ["A password", "A loop name", "A database index", "A web browser"]),
        ("Which HTML attribute specifies the URL of a link?", "href", ["src", "alt", "title", "id"]),
        ("Which CSS property controls the font size of text?", "font-size", ["text-size", "font-style", "font-weight", "letter-spacing"]),
    ]
    questions.extend(programming_facts)
    return [_make_question(question, correct, wrongs, index) for index, (question, correct, wrongs) in enumerate(questions[:100])]


def _make_geography_questions():
    questions = []

    capitals = [
        ("France", "Paris"),
        ("Japan", "Tokyo"),
        ("Australia", "Canberra"),
        ("Canada", "Ottawa"),
        ("Brazil", "Brasília"),
        ("India", "New Delhi"),
        ("China", "Beijing"),
        ("Italy", "Rome"),
        ("Germany", "Berlin"),
        ("Spain", "Madrid"),
        ("Portugal", "Lisbon"),
        ("Greece", "Athens"),
        ("Egypt", "Cairo"),
        ("Kenya", "Nairobi"),
        ("South Africa", "Pretoria"),
        ("Argentina", "Buenos Aires"),
        ("Mexico", "Mexico City"),
        ("United States", "Washington, D.C."),
        ("United Kingdom", "London"),
        ("Ireland", "Dublin"),
        ("Norway", "Oslo"),
        ("Sweden", "Stockholm"),
        ("Finland", "Helsinki"),
        ("Denmark", "Copenhagen"),
        ("Netherlands", "Amsterdam"),
        ("Belgium", "Brussels"),
        ("Switzerland", "Bern"),
        ("Austria", "Vienna"),
        ("Poland", "Warsaw"),
        ("Thailand", "Bangkok"),
        ("South Korea", "Seoul"),
        ("Indonesia", "Jakarta"),
        ("New Zealand", "Wellington"),
        ("Turkey", "Ankara"),
        ("Russia", "Moscow"),
        ("Chile", "Santiago"),
        ("Peru", "Lima"),
        ("Colombia", "Bogotá"),
        ("Saudi Arabia", "Riyadh"),
        ("Vietnam", "Hanoi"),
    ]
    capital_wrongs = [capital for _, capital in capitals]
    for country, capital in capitals:
        questions.append((f"What is the capital of {country}?", capital, capital_wrongs))

    geography_facts = [
        ("Which country is the largest by land area?", "Russia", ["Canada", "China", "United States", "Brazil"]),
        ("Which ocean is the largest?", "Pacific Ocean", ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Southern Ocean"]),
        ("Which ocean is the deepest?", "Pacific Ocean", ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Southern Ocean"]),
        ("Which mountain range contains Mount Everest?", "Himalayas", ["Rockies", "Alps", "Andes", "Atlas"]),
        ("Which continent is the smallest by land area?", "Australia", ["Europe", "Africa", "South America", "Asia"]),
        ("Which continent is the largest by land area?", "Asia", ["Africa", "North America", "Europe", "Australia"]),
        ("Which desert is the largest hot desert?", "Sahara Desert", ["Gobi Desert", "Arabian Desert", "Kalahari Desert", "Thar Desert"]),
        ("Which river is commonly cited as the longest river in the world?", "Nile River", ["Amazon River", "Yangtze River", "Mississippi River", "Danube River"]),
        ("Which river flows through Egypt?", "Nile River", ["Amazon River", "Danube River", "Ganges River", "Rhine River"]),
        ("Which river flows through London?", "Thames", ["Seine", "Tiber", "Rhine", "Danube"]),
        ("Which river flows through Paris?", "Seine", ["Thames", "Tiber", "Danube", "Rhine"]),
        ("Which sea separates Europe and Africa?", "Mediterranean Sea", ["Caribbean Sea", "Baltic Sea", "Red Sea", "North Sea"]),
        ("Which canal connects the Mediterranean Sea and Red Sea?", "Suez Canal", ["Panama Canal", "Erie Canal", "Kiel Canal", "Grand Canal"]),
        ("Which canal connects the Atlantic and Pacific Oceans?", "Panama Canal", ["Suez Canal", "Kiel Canal", "Erie Canal", "Grand Canal"]),
        ("Which country has the Great Barrier Reef?", "Australia", ["Indonesia", "Fiji", "New Zealand", "Japan"]),
        ("Which Australian state is Perth located in?", "Western Australia", ["Queensland", "Victoria", "Tasmania", "New South Wales"]),
        ("Which city is known as the Big Apple?", "New York City", ["Los Angeles", "Chicago", "Boston", "San Francisco"]),
        ("Which line divides Earth into Northern and Southern Hemispheres?", "Equator", ["Prime Meridian", "Tropic of Cancer", "Arctic Circle", "International Date Line"]),
        ("Which line is at 0 degrees longitude?", "Prime Meridian", ["Equator", "Tropic of Capricorn", "Antarctic Circle", "Arctic Circle"]),
        ("Which imaginary line is at about 23.5° N?", "Tropic of Cancer", ["Tropic of Capricorn", "Equator", "Prime Meridian", "Arctic Circle"]),
        ("Which imaginary line is at about 23.5° S?", "Tropic of Capricorn", ["Tropic of Cancer", "Equator", "Prime Meridian", "Antarctic Circle"]),
        ("Which country is both a country and a continent?", "Australia", ["Greenland", "Iceland", "Madagascar", "New Zealand"]),
        ("Which is the largest island in the world that is not a continent?", "Greenland", ["Borneo", "Madagascar", "New Guinea", "Iceland"]),
        ("Which country is shaped like a boot?", "Italy", ["Spain", "Greece", "Portugal", "France"]),
        ("Which country is known for fjords along its western coast?", "Norway", ["Egypt", "Brazil", "India", "Mexico"]),
        ("Which mountain is the highest above sea level?", "Mount Everest", ["K2", "Kilimanjaro", "Denali", "Aconcagua"]),
        ("Which mountain is the highest in Africa?", "Kilimanjaro", ["Mount Everest", "Denali", "Aconcagua", "Mont Blanc"]),
        ("Which mountain is the highest in South America?", "Aconcagua", ["Kilimanjaro", "Denali", "Mont Blanc", "K2"]),
        ("Which country contains Machu Picchu?", "Peru", ["Chile", "Mexico", "Colombia", "Argentina"]),
        ("Which country contains the Taj Mahal?", "India", ["Pakistan", "Bangladesh", "Nepal", "Sri Lanka"]),
        ("Which continent contains the Amazon Rainforest?", "South America", ["Africa", "Asia", "Europe", "Australia"]),
        ("Which continent contains the Sahara Desert?", "Africa", ["Asia", "Australia", "Europe", "South America"]),
        ("Which country has the city of Rio de Janeiro?", "Brazil", ["Argentina", "Chile", "Peru", "Colombia"]),
        ("Which U.S. state is known as the Sunshine State?", "Florida", ["California", "Texas", "Arizona", "Nevada"]),
        ("Which U.S. state is the largest by area?", "Alaska", ["Texas", "California", "Montana", "Florida"]),
        ("Which Canadian province has Toronto?", "Ontario", ["Quebec", "Alberta", "Manitoba", "British Columbia"]),
        ("Which Canadian province has Montreal?", "Quebec", ["Ontario", "British Columbia", "Nova Scotia", "Alberta"]),
        ("Which country has the city of Barcelona?", "Spain", ["Portugal", "France", "Italy", "Greece"]),
        ("Which country has the city of Munich?", "Germany", ["Austria", "Switzerland", "Poland", "Belgium"]),
        ("Which country has the city of Mumbai?", "India", ["Pakistan", "Sri Lanka", "Nepal", "Bangladesh"]),
        ("Which country has the city of Shanghai?", "China", ["Japan", "Vietnam", "South Korea", "Thailand"]),
        ("Which country has the city of Auckland?", "New Zealand", ["Australia", "Fiji", "Samoa", "Tonga"]),
        ("Which country has the city of Cape Town?", "South Africa", ["Kenya", "Egypt", "Morocco", "Ghana"]),
        ("Which country has the city of Istanbul?", "Turkey", ["Greece", "Egypt", "Italy", "Bulgaria"]),
        ("Which body of water lies between Saudi Arabia and Africa?", "Red Sea", ["Black Sea", "Caspian Sea", "Baltic Sea", "North Sea"]),
        ("Which body of water lies between Iran and Saudi Arabia?", "Persian Gulf", ["Mediterranean Sea", "Caribbean Sea", "North Sea", "Baltic Sea"]),
        ("Which region is the Arctic located around?", "North Pole", ["South Pole", "Equator", "Prime Meridian", "Tropic of Cancer"]),
        ("Which region is Antarctica located around?", "South Pole", ["North Pole", "Equator", "Tropic of Cancer", "Prime Meridian"]),
        ("Which country is famous for the Pyramids of Giza?", "Egypt", ["Greece", "Mexico", "India", "Italy"]),
        ("Which country is famous for the Eiffel Tower?", "France", ["Italy", "Spain", "Germany", "Belgium"]),
        ("Which country is famous for the Colosseum in Rome?", "Italy", ["Greece", "Turkey", "France", "Spain"]),
        ("Which lake is the largest freshwater lake by surface area?", "Lake Superior", ["Lake Victoria", "Lake Baikal", "Lake Michigan", "Lake Tanganyika"]),
        ("Which lake is the deepest in the world?", "Lake Baikal", ["Lake Superior", "Lake Victoria", "Lake Tanganyika", "Lake Michigan"]),
        ("Which country contains most of the Amazon River basin?", "Brazil", ["Argentina", "Chile", "Uruguay", "Paraguay"]),
        ("Which continent has the most countries?", "Africa", ["Asia", "Europe", "South America", "Australia"]),
        ("Which hemisphere is Australia mostly in?", "Southern Hemisphere", ["Northern Hemisphere", "Western Hemisphere only", "Eastern Hemisphere only", "Arctic Hemisphere"]),
        ("Which direction is usually at the top of a standard map?", "North", ["South", "East", "West", "Down"]),
        ("What is a peninsula?", "Land surrounded by water on three sides", ["A mountain top", "A desert lake", "A river delta only", "A glacier"]),
        ("What is an archipelago?", "A group of islands", ["A mountain range", "A desert", "A river mouth", "A plateau"]),
        ("What is a delta?", "Landform at a river mouth", ["A mountain peak", "An ocean trench", "A desert dune", "A glacier only"]),
    ]
    questions.extend(geography_facts)
    return [_make_question(question, correct, wrongs, index) for index, (question, correct, wrongs) in enumerate(questions[:100])]


def _make_math_questions():
    questions = []

    arithmetic = [
        ("7 + 8", "15", ["14", "16", "18", "13"]),
        ("12 + 9", "21", ["19", "20", "22", "23"]),
        ("25 + 17", "42", ["40", "41", "43", "44"]),
        ("64 - 28", "36", ["34", "35", "37", "38"]),
        ("90 - 45", "45", ["35", "40", "50", "55"]),
        ("13 × 6", "78", ["68", "72", "76", "84"]),
        ("9 × 9", "81", ["72", "80", "90", "99"]),
        ("144 ÷ 12", "12", ["10", "11", "13", "14"]),
        ("121 ÷ 11", "11", ["9", "10", "12", "13"]),
        ("31 + 19", "50", ["48", "49", "51", "52"]),
        ("72 ÷ 8", "9", ["6", "7", "8", "10"]),
        ("14 × 5", "70", ["60", "65", "75", "80"]),
        ("100 - 37", "63", ["53", "57", "67", "73"]),
        ("11 × 12", "132", ["121", "122", "144", "152"]),
        ("96 ÷ 6", "16", ["14", "15", "17", "18"]),
        ("56 + 29", "85", ["75", "84", "86", "95"]),
        ("83 - 27", "56", ["46", "54", "58", "60"]),
        ("15 × 15", "225", ["215", "220", "230", "250"]),
        ("18 + 4", "22", ["20", "21", "23", "24"]),
        ("16 + 16", "32", ["30", "31", "33", "34"]),
    ]
    for expression, answer, wrongs in arithmetic:
        questions.append((f"What is {expression}?", answer, wrongs))

    for number, answer in [(4, 16), (5, 25), (6, 36), (7, 49), (8, 64), (9, 81), (10, 100), (11, 121), (12, 144), (13, 169)]:
        questions.append((f"What is {number} squared?", str(answer), [str(answer + number), str(answer - number), str(number * 2), str(answer + 1)]))

    for number, answer in [(27, 3), (64, 4), (125, 5), (216, 6), (343, 7), (512, 8), (729, 9), (1000, 10)]:
        questions.append((f"What is the cube root of {number}?", str(answer), [str(answer + 1), str(answer - 1), str(answer * 2), str(answer + 3)]))

    math_facts = [
        ("What is the value of pi approximately?", "3.14", ["2.71", "1.62", "1.41", "4.13"]),
        ("What is the square root of 144?", "12", ["10", "14", "16", "18"]),
        ("What is 15% of 200?", "30", ["20", "25", "35", "40"]),
        ("What is the area of a circle with radius 5?", "25π", ["10π", "50π", "75π", "100π"]),
        ("What is 2 cubed?", "8", ["4", "6", "16", "32"]),
        ("What is the derivative of x²?", "2x", ["x", "x²", "2", "x³"]),
        ("What is the sum of angles in a triangle?", "180°", ["90°", "270°", "360°", "45°"]),
        ("What is log base 10 of 100?", "2", ["1", "10", "100", "0"]),
        ("What is 5 factorial?", "120", ["60", "24", "720", "100"]),
        ("Which formula is the Pythagorean theorem?", "a² + b² = c²", ["a + b = c", "a × b = c", "a ÷ b = c", "a² - b² = c²"]),
        ("What is the perimeter of a square with side length 6?", "24", ["12", "18", "30", "36"]),
        ("What is the area of a square with side length 9?", "81", ["18", "36", "72", "90"]),
        ("What is the area of a rectangle 8 by 5?", "40", ["13", "26", "80", "45"]),
        ("What is the perimeter of a rectangle 8 by 5?", "26", ["13", "40", "80", "30"]),
        ("What is the area of a triangle with base 10 and height 6?", "30", ["16", "60", "100", "36"]),
        ("What is the volume of a cube with side length 3?", "27", ["9", "18", "81", "12"]),
        ("How many degrees are in a right angle?", "90°", ["45°", "180°", "360°", "60°"]),
        ("How many degrees are in a straight angle?", "180°", ["45°", "90°", "360°", "270°"]),
        ("How many sides does a hexagon have?", "6", ["5", "7", "8", "9"]),
        ("How many sides does an octagon have?", "8", ["6", "7", "9", "10"]),
        ("Solve for x: x + 7 = 12", "5", ["3", "4", "6", "7"]),
        ("Solve for x: 2x = 18", "9", ["6", "7", "8", "10"]),
        ("Solve for x: x - 4 = 10", "14", ["6", "10", "16", "20"]),
        ("Solve for x: 3x = 21", "7", ["5", "6", "8", "9"]),
        ("Solve for x: x/5 = 4", "20", ["9", "15", "25", "30"]),
        ("What is the slope of y = 3x + 2?", "3", ["2", "5", "-3", "0"]),
        ("What is the y-intercept of y = 4x - 7?", "-7", ["4", "7", "0", "-4"]),
        ("What is x² × x³?", "x⁵", ["x⁶", "x⁹", "2x⁵", "x"]),
        ("What is x⁶ ÷ x²?", "x⁴", ["x²", "x³", "x⁸", "x¹²"]),
        ("What is (x + 2)(x + 3)?", "x² + 5x + 6", ["x² + 6x + 5", "x² + 2x + 3", "2x + 5", "x² + 6"]),
        ("What is the mean of 2, 4, 6, and 8?", "5", ["4", "6", "8", "10"]),
        ("What is the median of 3, 7, 9?", "7", ["3", "9", "19", "6"]),
        ("What is the mode of 1, 2, 2, 3, 4?", "2", ["1", "3", "4", "5"]),
        ("What is the range of 5, 9, 11, 20?", "15", ["11", "20", "25", "9"]),
        ("What is the probability of flipping heads on a fair coin?", "1/2", ["0", "1/4", "1", "2"]),
        ("What is the probability of rolling a 6 on a fair six-sided die?", "1/6", ["1/2", "1/3", "1/12", "1"]),
        ("How many outcomes are possible when flipping two coins?", "4", ["2", "3", "6", "8"]),
        ("What is 25% written as a decimal?", "0.25", ["0.5", "2.5", "25.0", "0.025"]),
        ("What is 0.75 written as a fraction?", "3/4", ["1/4", "1/2", "4/3", "2/3"]),
        ("What is 3/5 as a decimal?", "0.6", ["0.3", "0.5", "0.8", "0.35"]),
        ("What is 40% of 50?", "20", ["10", "30", "40", "25"]),
        ("What is 12.5% of 80?", "10", ["8", "12", "16", "20"]),
        ("What is the next prime number after 7?", "11", ["8", "9", "10", "12"]),
        ("Which number is prime?", "29", ["21", "35", "49", "39"]),
        ("What is the greatest common factor of 12 and 18?", "6", ["3", "9", "12", "18"]),
        ("What is the least common multiple of 4 and 6?", "12", ["8", "10", "24", "6"]),
        ("What is |−9|?", "9", ["-9", "0", "18", "1"]),
        ("What is −3 + 8?", "5", ["-11", "-5", "11", "8"]),
        ("What is −4 × 6?", "-24", ["-10", "10", "24", "-20"]),
        ("What is 10 to the power of 3?", "1000", ["30", "100", "10000", "300"]),
        ("What is 2⁵?", "32", ["10", "16", "25", "64"]),
        ("What is the reciprocal of 4?", "1/4", ["4", "-4", "0.4", "2"]),
        ("What is the circumference of a circle with radius r?", "2πr", ["πr²", "2r", "πd²", "r²"]),
        ("What is the area of a circle with radius r?", "πr²", ["2πr", "πd", "r²", "2r"]),
        ("Which graph represents a linear equation?", "A straight line", ["A circle only", "A parabola only", "A random scatter only", "A cube"]),
        ("Which graph is typical for y = x²?", "Parabola", ["Line", "Circle", "Hyperbola only", "Scatterplot only"]),
        ("What is the value of 0 divided by 5?", "0", ["1", "5", "Undefined", "10"]),
        ("What is division by zero?", "Undefined", ["0", "1", "Always 10", "-1"]),
        ("What is the sum of exterior angles of any polygon?", "360°", ["90°", "180°", "270°", "720°"]),
        ("How many degrees are in a full circle?", "360°", ["90°", "180°", "270°", "400°"]),
        ("What type of equations does the quadratic formula solve?", "Quadratic equations", ["Linear equations", "Only fractions", "Only angles", "Only percentages"]),
        ("What is the absolute value of 12?", "12", ["-12", "0", "24", "6"]),
        ("What is 1/2 + 1/4?", "3/4", ["1/4", "1/2", "1", "2/4"]),
        ("What is 2/3 + 1/3?", "1", ["1/3", "2/3", "3", "4/3"]),
    ]
    questions.extend(math_facts)
    return [_make_question(question, correct, wrongs, index) for index, (question, correct, wrongs) in enumerate(questions[:100])]


def _make_biology_questions():
    biology_facts = [
        ("What is the powerhouse of the cell?", "Mitochondria", ["Nucleus", "Ribosome", "Endoplasmic reticulum", "Golgi apparatus"]),
        ("Which molecule carries genetic information?", "DNA", ["Protein", "Carbohydrate", "Lipid", "Water"]),
        ("What is the process by which plants make food?", "Photosynthesis", ["Respiration", "Transpiration", "Fermentation", "Digestion"]),
        ("Which organelle is responsible for protein synthesis?", "Ribosome", ["Golgi apparatus", "Lysosome", "Vacuole", "Nucleus"]),
        ("What is the basic unit of life?", "Cell", ["Atom", "Molecule", "Tissue", "Organ"]),
        ("Which blood cells fight infections?", "White blood cells", ["Red blood cells", "Platelets", "Plasma", "Neurons"]),
        ("What is cell division in somatic cells called?", "Mitosis", ["Meiosis", "Binary fission", "Budding", "Fertilisation"]),
        ("Which vitamin is produced by skin exposed to sunlight?", "Vitamin D", ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin K"]),
        ("What is the largest organ of the human body?", "Skin", ["Heart", "Liver", "Brain", "Lungs"]),
        ("Which blood vessel carries blood away from the heart?", "Artery", ["Vein", "Capillary", "Venule", "Alveolus"]),
        ("Which organ pumps blood through the body?", "Heart", ["Lungs", "Kidney", "Stomach", "Pancreas"]),
        ("Which organ is mainly responsible for gas exchange?", "Lungs", ["Liver", "Pancreas", "Spleen", "Kidney"]),
        ("Which organ filters blood and produces urine?", "Kidney", ["Heart", "Brain", "Stomach", "Liver"]),
        ("Which organ produces insulin?", "Pancreas", ["Liver", "Kidney", "Stomach", "Spleen"]),
        ("Which organ controls most body activities?", "Brain", ["Heart", "Liver", "Skin", "Small intestine"]),
        ("What is the liquid part of blood called?", "Plasma", ["Platelet", "Neuron", "Cartilage", "Bone marrow"]),
        ("Which blood cells carry oxygen?", "Red blood cells", ["White blood cells", "Platelets", "Plasma", "Neurons"]),
        ("Which blood component helps clotting?", "Platelets", ["Neurons", "Hormones", "Antibodies only", "Red blood cells only"]),
        ("What protein in red blood cells carries oxygen?", "Hemoglobin", ["Insulin", "Keratin", "Collagen", "Amylase"]),
        ("Which system includes the brain and spinal cord?", "Nervous system", ["Digestive system", "Skeletal system", "Endocrine system", "Respiratory system"]),
        ("Which system breaks down food?", "Digestive system", ["Respiratory system", "Nervous system", "Muscular system", "Skeletal system"]),
        ("Which system supports the body with bones?", "Skeletal system", ["Endocrine system", "Immune system", "Respiratory system", "Digestive system"]),
        ("Which system helps defend against disease?", "Immune system", ["Skeletal system", "Digestive system", "Integumentary system", "Muscular system"]),
        ("What is the main function of roots in plants?", "Absorb water and minerals", ["Make seeds only", "Attract pollinators only", "Produce oxygen only", "Make pollen only"]),
        ("Which plant structure absorbs most light for photosynthesis?", "Leaf", ["Root", "Seed", "Stem only", "Flower only"]),
        ("Which pigment makes many plants green?", "Chlorophyll", ["Hemoglobin", "Melanin", "Keratin", "Insulin"]),
        ("What gas do plants release during photosynthesis?", "Oxygen", ["Nitrogen", "Hydrogen", "Methane", "Carbon monoxide"]),
        ("What sugar is produced during photosynthesis?", "Glucose", ["Lactose", "Starch only", "Cellulose only", "Sucrose only"]),
        ("What is the male reproductive part of a flower?", "Stamen", ["Pistil", "Petal", "Sepal", "Ovary"]),
        ("What is the female reproductive part of a flower?", "Pistil", ["Stamen", "Petal", "Sepal", "Filament"]),
        ("What is pollination?", "Transfer of pollen", ["Breaking down food", "Cell division", "Water evaporation", "Blood clotting"]),
        ("What are genes made of?", "DNA", ["Starch", "Fat", "Water only", "Cellulose"]),
        ("Where is DNA mainly found in eukaryotic cells?", "Nucleus", ["Cell wall", "Ribosome", "Chloroplast only", "Cytoplasm only"]),
        ("How many chromosomes are in most human body cells?", "46", ["23", "64", "92", "44"]),
        ("How many chromosomes are in a typical human gamete?", "23", ["46", "64", "92", "22"]),
        ("What is meiosis used to produce?", "Gametes", ["Skin cells", "Muscle fibres", "Red blood cells only", "Bone cells"]),
        ("What is a mutation?", "A change in DNA sequence", ["A type of organ", "A food molecule", "A plant root", "A blood vessel"]),
        ("What is heredity?", "Passing traits from parents to offspring", ["Breathing oxygen", "Digesting proteins", "Making energy in muscles", "Breaking down waste"]),
        ("Who is known for early laws of inheritance from pea plants?", "Gregor Mendel", ["Charles Darwin", "Louis Pasteur", "Rosalind Franklin", "Isaac Newton"]),
        ("What is natural selection?", "Differential survival and reproduction", ["Random food choice", "Cell copying only", "A type of photosynthesis", "Protein digestion"]),
        ("Who proposed evolution by natural selection?", "Charles Darwin", ["Isaac Newton", "Albert Einstein", "Marie Curie", "Gregor Mendel"]),
        ("What is an ecosystem?", "Living organisms and their environment", ["One animal only", "Only a climate zone", "Only a food chain", "A single cell"]),
        ("What is a producer in an ecosystem?", "An organism that makes its own food", ["An organism that eats only meat", "A decomposer only", "A parasite only", "A predator only"]),
        ("What is a consumer in an ecosystem?", "An organism that eats other organisms", ["A plant making glucose", "A rock layer", "Sunlight", "Water"]),
        ("What is a decomposer?", "Organism that breaks down dead matter", ["Organism that makes light", "A large predator only", "A seed only", "A herbivore only"]),
        ("Which organism is a common decomposer?", "Fungus", ["Eagle", "Grass", "Rabbit", "Kangaroo"]),
        ("What is a herbivore?", "Animal that eats plants", ["Animal that eats meat", "Animal that eats plants and meat", "Plant that eats insects", "Animal that eats fungi only"]),
        ("What is a carnivore?", "Animal that eats meat", ["Animal that eats plants", "Organism that makes its own food", "Bacterium only", "Animal that eats nectar only"]),
        ("What is an omnivore?", "Animal that eats plants and animals", ["Animal that eats only plants", "Animal that eats only meat", "Plant that makes seeds", "Fungus that decomposes wood"]),
        ("What does a food chain show?", "Energy flow between organisms", ["Rock formation", "Water boiling", "Blood pressure only", "Cloud formation"]),
        ("What is biodiversity?", "Variety of living things", ["Amount of rainfall only", "A single species", "A type of cell", "A blood type"]),
        ("What is a habitat?", "Place where an organism lives", ["A type of gene", "A blood cell", "A digestive enzyme", "A cell organelle"]),
        ("What is a niche?", "An organism&apos;s role in its ecosystem", ["A bone joint", "A leaf vein", "A protein shape only", "A type of sugar"]),
        ("What is homeostasis?", "Maintaining stable internal conditions", ["Making sunlight", "Changing species instantly", "Digesting only fats", "Growing seeds only"]),
        ("What hormone lowers blood glucose?", "Insulin", ["Adrenaline", "Melatonin", "Thyroxine", "Estrogen"]),
        ("What hormone is associated with fight-or-flight responses?", "Adrenaline", ["Insulin", "Estrogen", "Testosterone only", "Melatonin"]),
        ("What are enzymes?", "Biological catalysts", ["Bone cells", "Blood vessels", "Plant pigments only", "Genetic codes"]),
        ("What is respiration in cells used for?", "Releasing energy from glucose", ["Making pollen", "Absorbing sunlight only", "Producing DNA only", "Making bones"]),
        ("What is aerobic respiration?", "Respiration using oxygen", ["Respiration without oxygen", "Photosynthesis in roots", "Digestion in the stomach", "Cell division only"]),
        ("What is anaerobic respiration?", "Respiration without oxygen", ["Respiration using oxygen", "Blood clotting", "Protein synthesis", "Bone growth"]),
        ("What is fermentation?", "Anaerobic breakdown of sugars", ["Copying DNA", "Pumping blood", "Moving water through xylem only", "Filtering blood"]),
        ("Which organelle contains chlorophyll in plant cells?", "Chloroplast", ["Mitochondrion", "Nucleus", "Ribosome", "Lysosome"]),
        ("Which structure surrounds a plant cell but not an animal cell?", "Cell wall", ["Cell membrane", "Cytoplasm", "Nucleus", "Mitochondrion"]),
        ("What controls what enters and leaves a cell?", "Cell membrane", ["Cell wall only", "Nucleus only", "Ribosome", "Vacuole only"]),
        ("What is cytoplasm?", "Jelly-like material inside cells", ["A bone tissue", "A blood protein", "A plant hormone", "A DNA base"]),
        ("What is the function of the nucleus?", "Controls cell activities", ["Makes cell walls", "Stores oxygen", "Digests food only", "Pumps blood"]),
        ("What organelle modifies and packages proteins?", "Golgi apparatus", ["Ribosome", "Nucleus", "Lysosome", "Cell wall"]),
        ("What organelle digests waste materials in many cells?", "Lysosome", ["Chloroplast", "Nucleus", "Cell wall", "Ribosome"]),
        ("What is diffusion?", "Movement from high to low concentration", ["Movement of blood in arteries", "Cell division", "DNA copying", "Bone growth"]),
        ("What is osmosis?", "Diffusion of water across a membrane", ["Movement of oxygen in lungs only", "Digestion of proteins", "Production of gametes", "Transfer of pollen"]),
        ("What is taxonomy?", "Classification of organisms", ["Study of earthquakes", "Measurement of pressure", "Study of weather only", "Study of stars"]),
        ("What is the two-part scientific naming system called?", "Binomial nomenclature", ["Photosynthesis", "Homeostasis", "Mitosis", "Osmosis"]),
        ("What is the highest taxonomic rank in the common modern hierarchy?", "Domain", ["Species", "Genus", "Family", "Order"]),
        ("What taxonomic rank comes below genus?", "Species", ["Family", "Order", "Class", "Domain"]),
        ("Which group includes mammals, birds, reptiles, amphibians, and fish?", "Vertebrates", ["Fungi", "Plants", "Bacteria only", "Protists only"]),
        ("What do vertebrates have?", "Backbone", ["Cell wall", "Chlorophyll", "Six legs always", "Pollen"]),
        ("Which animals are warm-blooded and usually have hair or fur?", "Mammals", ["Reptiles", "Amphibians", "Fish", "Insects"]),
        ("Which animals usually have feathers?", "Birds", ["Mammals", "Reptiles", "Fish", "Amphibians"]),
        ("Which animals usually have scales and breathe with gills?", "Fish", ["Birds", "Mammals", "Amphibians only", "Reptiles only"]),
        ("Which animals live part of life in water and part on land?", "Amphibians", ["Birds", "Mammals", "Reptiles only", "Fish only"]),
        ("Which kingdom includes mushrooms?", "Fungi", ["Plants", "Animals", "Protists only", "Bacteria only"]),
        ("Which microorganisms can usually be killed by antibiotics?", "Bacteria", ["Viruses", "Fungi only", "Algae only", "Plants"]),
        ("What is a virus?", "Infectious particle needing a host cell", ["A type of plant root", "A blood cell", "A mineral", "A bone cell"]),
        ("What is vaccination used for?", "Training the immune system", ["Digesting food faster", "Increasing bone length", "Making oxygen", "Breaking down starch"]),
        ("What are antibodies?", "Proteins that help identify pathogens", ["Sugars in plants", "Bone minerals", "Digestive wastes", "Plant pigments"]),
        ("What is the scientific study of plants called?", "Botany", ["Zoology", "Geology", "Astronomy", "Meteorology"]),
        ("What is the scientific study of animals called?", "Zoology", ["Botany", "Meteorology", "Chemistry", "Geology"]),
        ("Which part of the digestive system absorbs most nutrients?", "Small intestine", ["Stomach", "Large intestine", "Esophagus", "Mouth"]),
        ("Which organ produces bile?", "Liver", ["Pancreas", "Kidney", "Heart", "Lungs"]),
        ("What is the main function of xylem in plants?", "Transport water", ["Transport sugars", "Make pollen", "Store DNA", "Digest food"]),
        ("What is the main function of phloem in plants?", "Transport sugars", ["Transport water", "Pump blood", "Make bones", "Filter urine"]),
        ("What is a stimulus?", "A change an organism responds to", ["A permanent bone", "A type of sugar", "A plant seed only", "A blood vessel"]),
        ("What is a reflex action?", "Fast automatic response", ["Slow planned movement", "Photosynthesis", "Digestion of fats", "DNA replication only"]),
        ("Which part of the eye detects light?", "Retina", ["Iris", "Cornea", "Lens", "Pupil"]),
        ("Which part of the ear helps with balance?", "Semicircular canals", ["Eardrum", "Cochlea only", "Ear canal", "Hammer bone only"]),
        ("What type of joint is the shoulder?", "Ball-and-socket joint", ["Hinge joint", "Fixed joint", "Pivot joint", "Gliding joint only"]),
        ("What type of joint is the elbow?", "Hinge joint", ["Ball-and-socket joint", "Fixed joint", "Saddle joint", "Immovable joint"]),
        ("What is the process by which plants lose water vapor through leaves?", "Transpiration", ["Respiration", "Photosynthesis", "Germination", "Osmosis"]),
        ("Which macromolecule is the main source of energy for cells?", "Carbohydrate", ["Protein", "Lipid", "Nucleic acid", "Vitamin"]),
        ("What is the term for blood vessels that carry blood to the heart?", "Veins", ["Arteries", "Capillaries", "Venules", "Aorta"]),
    ]
    return [_make_question(question, correct, wrongs, index) for index, (question, correct, wrongs) in enumerate(biology_facts[:100])]


def _quiz_banks():
    quiz_banks = {
        "Science": _make_science_questions(),
        "Programming": _make_programming_questions(),
        "Math": _make_math_questions(),
        "Geography": _make_geography_questions(),
        "Biology": _make_biology_questions(),
    }

    for category, questions in quiz_banks.items():
        if len(questions) != 100:
            raise ValueError(f"{category} must have exactly 100 questions; found {len(questions)}")

    return quiz_banks


def add_sample_quizzes():
    """
    Add sample quizzes until each category has 100 questions.

    This is safer than checking only Quiz.query.count(), because it prevents one
    category from blocking another category that still needs more questions.
    """
    quiz_banks = _quiz_banks()

    for category, questions in quiz_banks.items():
        existing_count = Quiz.query.filter_by(category=category).count()
        if existing_count >= 100:
            continue

        for question_data in questions[existing_count:100]:
            db.session.add(Quiz(category=category, **question_data))

    db.session.commit()


def find_registered_user_by_id(user_id):
    return db.session.get(RegisteredUser, user_id)
