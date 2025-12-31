
import sqlite3

conn = sqlite3.connect("quizmaster.db")
cursor = conn.cursor()

# USERS TABLE WITH ROLE 
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL,
               name TEXT NOT NULL,
               role TEXT NOT NULL CHECK(role IN ("user", "admin"))
)
""")

# QUIZES TABLE 
cursor.execute("""
CREATE TABLE IF NOT EXISTS quizzes (
               quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               subject TEXT NOT NULL,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# QUESTIONS TABLE 
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
               question_id INTEGER PRIMARY KEY AUTOINCREMENT,
               quiz_id INTEGER NOT NULL,
               question_text TEXT NOT NULL,
               option_a TEXT NOT NULL,
               option_b TEXT NOT NULL,
               option_c TEXT NOT NULL,
               option_d TEXT NOT NULL,
               correct_option TEXT,
               integer_answer INTEGER,
               image_path TEXT,
               question_type TEXT NOT NULL,
               FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
)
""")

cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?,?,?)", ("sakshamdora","SAKSHAM","admin"))

cursor.execute("INSERT OR IGNORE INTO quizzes (quiz_id, title, subject) VALUES (?,?,?)", (1,"PHYSICS QUIZ 1","Physics"))
cursor.execute("INSERT OR IGNORE INTO quizzes (quiz_id, title, subject) VALUES (?,?,?)", (2,"PHYSICS QUIZ 2","Physics"))
cursor.execute("INSERT OR IGNORE INTO quizzes (quiz_id, title, subject) VALUES (?,?,?)", (3,"PHYSICS QUIZ 3","Physics"))
cursor.execute("INSERT OR IGNORE INTO quizzes (quiz_id, title, subject) VALUES (?,?,?)", (4,"CHEMISTRY QUIZ 1","Chemistry"))
cursor.execute("INSERT OR IGNORE INTO quizzes (quiz_id, title, subject) VALUES (?,?,?)", (5,"CHEMISTRY QUIZ 2","Chemistry"))
cursor.execute("INSERT OR IGNORE INTO quizzes (quiz_id, title, subject) VALUES (?,?,?)", (6,"MATHS QUIZ 1","Maths"))
cursor.execute("INSERT OR IGNORE INTO quizzes (quiz_id, title, subject) VALUES (?,?,?)", (7,"CHEMISTRY QUIZ 3","Chemistry"))
cursor.execute("INSERT OR IGNORE INTO quizzes (quiz_id, title, subject) VALUES (?,?,?)", (8,"MATHS QUIZ 1","Maths"))
cursor.execute("INSERT OR IGNORE INTO quizzes (quiz_id, title, subject) VALUES (?,?,?)", (9,"MATHS QUIZ 1","Maths"))


questions = [
# ---------- MCQs (20) ----------
(1,'Unit of electric field is','N/C','V/m','J/C','Both A and B','d',None,None,'mcq'),
(1,'Dimensional formula of force is','MLT-1','MLT-2','ML2T-2','M2LT-2','c',None,None,'mcq'),
(1,'SI unit of magnetic flux is','Tesla','Weber','Henry','Gauss','b',None,None,'mcq'),
(1,'Value of g on moon is approximately','9.8','1.6','3.7','0','b',None,None,'mcq'),
(1,'Work done in circular motion is','maximum','minimum','zero','negative','c',None,None,'mcq'),
(1,'Ohms law is valid for','semiconductors','superconductors','conductors','all materials','c',None,None,'mcq'),
(1,'Speed of light in vacuum is','3e8 m/s','3e6 m/s','1.5e8 m/s','9.8 m/s','a',None,None,'mcq'),
(1,'Photon has','mass','charge','momentum','all','c',None,None,'mcq'),
(1,'Capacitance depends on','area','distance','dielectric','all','d',None,None,'mcq'),
(1,'Escape velocity depends on','mass','radius','both','none','c',None,None,'mcq'),
(1,'Lens used in microscope is','convex','concave','plane','none','a',None,None,'mcq'),
(1,'SI unit of current is','volt','ampere','ohm','watt','b',None,None,'mcq'),
(1,'Charge of electron is','positive','negative','zero','variable','b',None,None,'mcq'),
(1,'Energy stored in capacitor is','QV','CV','½CV²','½QV','c',None,None,'mcq'),
(1,'Time period of pendulum depends on','mass','length','amplitude','density','b',None,None,'mcq'),
(1,'Magnetic field inside solenoid is','zero','uniform','variable','infinite','b',None,None,'mcq'),
(1,'Unit of resistance is','volt','ampere','ohm','watt','c',None,None,'mcq'),
(1,'Nuclear forces are','weak','strong','electromagnetic','gravitational','b',None,None,'mcq'),
(1,'Sound cannot travel in','solid','liquid','gas','vacuum','d',None,None,'mcq'),
(1,'Power factor lies between','0 and 1','1 and 2','-1 and 1','0 only','a',None,None,'mcq'),

# ---------- Integer (5) ----------
(1,'Value of acceleration due to gravity on earth (approx)','None','None','None','None',None,10,None,'integer'),
(1,'Number of significant figures in 0.0050','None','None','None','None',None,2,None,'integer'),
(1,'Charge on proton in units of e','None','None','None','None',None,1,None,'integer'),
(1,'Dimension of velocity (power of T)','None','None','None','None',None,-1,None,'integer'),
(1,'Refractive index of vacuum','None','None','None','None',None,1,None,'integer'),

## ---------- CHEMISTRY QUESTIONS ----------##
# ---------- MCQs (20) ----------#
(4,'Atomic number represents number of','protons','neutrons','electrons','nucleons','a',None,None,'mcq'),
(4,'pH of pure water is','5','7','9','0','b',None,None,'mcq'),
(4,'Gas used in photosynthesis is','O2','CO2','N2','H2','b',None,None,'mcq'),
(4,'Strong acid among following is','CH3COOH','H2SO4','H2CO3','HNO2','b',None,None,'mcq'),
(4,'Hybridization in methane is','sp','sp2','sp3','dsp2','c',None,None,'mcq'),
(4,'Avogadro number is','6.02e23','3e8','1.6e-19','9.8','a',None,None,'mcq'),
(4,'Oxidation is','loss of e-','gain of e-','loss of H','gain of O','a',None,None,'mcq'),
(4,'SI unit of amount of substance is','gram','mole','kg','litre','b',None,None,'mcq'),
(4,'Catalyst affects','equilibrium','rate','yield','energy','b',None,None,'mcq'),
(4,'Hardest allotrope of carbon is','graphite','coal','diamond','fullerene','c',None,None,'mcq'),
(4,'Functional group in alcohol is','-COOH','-CHO','-OH','-NH2','c',None,None,'mcq'),
(4,'Rusting is','oxidation','reduction','neutralization','hydrolysis','a',None,None,'mcq'),
(4,'Bond in NaCl is','covalent','ionic','hydrogen','metallic','b',None,None,'mcq'),
(4,'p-block elements are','s and p','p and d','p only','d only','c',None,None,'mcq'),
(4,'Noble gases are','reactive','inert','metallic','toxic','b',None,None,'mcq'),
(4,'Electrolyte conducts in','solid','liquid','gas','vacuum','b',None,None,'mcq'),
(4,'Atomic radius decreases across period because of','shielding','nuclear charge','mass','electrons','b',None,None,'mcq'),
(4,'H2O molecule shape is','linear','trigonal','bent','tetrahedral','c',None,None,'mcq'),
(4,'Gas law PV = nRT is','Boyle','Charles','Ideal gas','Avogadro','c',None,None,'mcq'),
(4,'Oxidation number of O in H2O2 is','-2','-1','0','+2','b',None,None,'mcq'),

# ---------- Integer (5) ----------
(4,'Atomic number of oxygen','None','None','None','None',None,8,None,'integer'),
(4,'Valency of nitrogen','None','None','None','None',None,3,None,'integer'),
(4,'pH of neutral solution','None','None','None','None',None,7,None,'integer'),
(4,'Number of atoms in O2 molecule','None','None','None','None',None,2,None,'integer'),
(4,'Molar mass of hydrogen','None','None','None','None',None,1,None,'integer'),

## ---------- MATHEMATICS QUESTIONS ----------##
# ---------- MCQs (20) ----------
(6,'Derivative of x²','2x','x','x²','1','a',None,None,'mcq'),
(6,'Value of sin 90°','0','1','-1','∞','b',None,None,'mcq'),
(6,'Slope of y=5','0','5','1','undefined','a',None,None,'mcq'),
(6,'Value of log₁₀1','0','1','10','∞','a',None,None,'mcq'),
(6,'Integral of 1 dx','x','1','0','x²','a',None,None,'mcq'),
(6,'Distance formula is','√(x²+y²)','√((x2-x1)²+(y2-y1)²)','x+y','|x-y|','b',None,None,'mcq'),
(6,'Quadratic equation degree is','1','2','3','4','b',None,None,'mcq'),
(6,'sin²θ + cos²θ =','0','1','2','θ','b',None,None,'mcq'),
(6,'Number of solutions of linear equation','0','1','2','infinite','d',None,None,'mcq'),
(6,'Value of i²','-1','1','0','i','a',None,None,'mcq'),
(6,'Mean of 2 and 8','4','5','6','8','b',None,None,'mcq'),
(6,'Determinant of identity matrix','0','1','2','n','b',None,None,'mcq'),
(6,'tan 45°','0','1','√3','∞','b',None,None,'mcq'),
(6,'If A∩B = Ø then A and B are','equal','disjoint','subset','universal','b',None,None,'mcq'),
(6,'Sum of angles of triangle','90°','180°','360°','270°','b',None,None,'mcq'),
(6,'Value of |−5|','-5','5','0','1','b',None,None,'mcq'),
(6,'Logarithm base e is called','common','binary','natural','complex','c',None,None,'mcq'),
(6,'Area of circle','2πr','πr²','πd','r²','b',None,None,'mcq'),
(6,'Solution of x=|x|','x≥0','x≤0','all x','none','a',None,None,'mcq'),
(6,'Matrix with equal rows and columns is','square','row','column','None','a',None,None,'mcq'),

# ---------- Integer (5) ----------
(6,'Value of 2² + 3²','None','None','None','None',None,13,None,'integer'),
(6,'Degree of polynomial x³','None','None','None','None',None,3,None,'integer'),
(6,'Value of sin 0°','None','None','None','None',None,0,None,'integer'),
(6,'Number of diagonals in triangle','None','None','None','None',None,0,None,'integer'),
(6,'Value of π (nearest integer)','None','None','None','None',None,3,None,'integer'),
## ------------- QUIZ-2---------------------##
# ----------PHYSICS QUIZ MCQs (20) ----------
(2,'SI unit of electric charge is','coulomb','ampere','volt','ohm','a',None,None,'mcq'),
(2,'Dimensional formula of energy is','ML2T-2','MLT-1','M2L2T-2','MLT-2','a',None,None,'mcq'),
(2,'Which particle has no charge','electron','proton','neutron','positron','c',None,None,'mcq'),
(2,'Velocity-time graph slope represents','distance','speed','acceleration','displacement','c',None,None,'mcq'),
(2,'Unit of power is','joule','watt','newton','volt','b',None,None,'mcq'),
(2,'Work done by centripetal force is','positive','negative','zero','infinite','c',None,None,'mcq'),
(2,'Magnetic field lines form','open curves','closed loops','straight lines','random paths','b',None,None,'mcq'),
(2,'Frequency unit is','hertz','second','meter','radian','a',None,None,'mcq'),
(2,'Momentum depends on','mass','velocity','both','none','c',None,None,'mcq'),
(2,'Which law explains buoyancy','Newton','Pascal','Archimedes','Bernoulli','c',None,None,'mcq'),
(2,'SI unit of pressure is','pascal','bar','atm','newton','a',None,None,'mcq'),
(2,'Heat transfer without medium is','conduction','convection','radiation','none','c',None,None,'mcq'),
(2,'Fuse wire works on principle of','heating effect','magnetism','chemical effect','pressure','a',None,None,'mcq'),
(2,'Electric power P =','VI','V/I','I/R','V²I','a',None,None,'mcq'),
(2,'Lens power unit is','diopter','meter','cm','watt','a',None,None,'mcq'),
(2,'Mirror used in headlights is','plane','convex','concave','cylindrical','c',None,None,'mcq'),
(2,'Nuclear energy source is','chemical','electrical','atomic','thermal','c',None,None,'mcq'),
(2,'Time period of wave depends on','frequency','amplitude','speed','wavelength','a',None,None,'mcq'),
(2,'Electric field inside conductor is','zero','maximum','variable','infinite','a',None,None,'mcq'),
(2,'Unit of inductance is','henry','weber','tesla','farad','a',None,None,'mcq'),

# ---------- Integer (5) ----------
(2,'Speed of light in vacuum ( x X 10^8 m/s)','None','None','None','None',None,3,None,'integer'),
(2,'Number of fundamental forces','None','None','None','None',None,4,None,'integer'),
(2,'Value of g on earth (approx)','None','None','None','None',None,10,None,'integer'),
(2,'Number of dimensions of space','None','None','None','None',None,3,None,'integer'),
(2,'Charge on electron (in units of e)','None','None','None','None',None,-1,None,'integer'),

## ------------- QUIZ-3---------------------##
# ---------- MCQs (20) ----------
(3,'Unit of magnetic field is','tesla','weber','henry','gauss','a',None,None,'mcq'),
(3,'Acceleration due to gravity is maximum at','equator','poles','tropics','sea','b',None,None,'mcq'),
(3,'Which wave is longitudinal','light','sound','radio','x-ray','b',None,None,'mcq'),
(3,'Energy of photon depends on','wavelength','frequency','speed','mass','b',None,None,'mcq'),
(3,'Resistance increases with','length','area','temperature decrease','thickness','a',None,None,'mcq'),
(3,'SI unit of capacitance is','farad','henry','ohm','coulomb','a',None,None,'mcq'),
(3,'Device that converts AC to DC','transformer','rectifier','inductor','capacitor','b',None,None,'mcq'),
(3,'Ohmic materials obey','Ohm’s law','Faraday law','Lenz law','Gauss law','a',None,None,'mcq'),
(3,'Which has highest speed','sound','light','electron','proton','b',None,None,'mcq'),
(3,'Force per unit area is','pressure','stress','energy','work','a',None,None,'mcq'),
(3,'Thermodynamics zero law defines','heat','temperature','work','energy','b',None,None,'mcq'),
(3,'SI unit of angular velocity','rad/s','m/s','degree','rpm','a',None,None,'mcq'),
(3,'AC frequency in India is','50 Hz','60 Hz','100 Hz','25 Hz','a',None,None,'mcq'),
(3,'Kinetic energy depends on','velocity','mass','both','none','c',None,None,'mcq'),
(3,'Which mirror gives virtual image always','concave','convex','plane','both b and c','d',None,None,'mcq'),
(3,'Radiation pressure is due to','mass','charge','momentum','heat','c',None,None,'mcq'),
(3,'Unit of electric potential is','volt','joule','ampere','ohm','a',None,None,'mcq'),
(3,'Earth magnetic field is due to','rotation','core currents','atmosphere','moon','b',None,None,'mcq'),
(3,'Capacitor blocks','dc','ac','both','none','a',None,None,'mcq'),
(3,'Photoelectric effect supports','wave theory','particle theory','relativity','string theory','b',None,None,'mcq'),

# ---------- Integer (5) ----------
(3,'Number of laws of thermodynamics','None','None','None','None',None,4,None,'integer'),
(3,'Dimensional power of time in velocity','None','None','None','None',None,-1,None,'integer'),
(3,'Refractive index of vacuum','None','None','None','None',None,1,None,'integer'),
(3,'Value of π (nearest integer)','None','None','None','None',None,3,None,'integer'),
(3,'Number of electrons in hydrogen atom','None','None','None','None',None,1,None,'integer'),

## ------------- QUIZ-5---------------------##
# ---------- MCQs (20) ----------
(5,'Atomic number is equal to number of','protons','neutrons','electrons only','nucleons','a',None,None,'mcq'),
(5,'pH of acidic solution is','less than 7','equal to 7','greater than 7','zero','a',None,None,'mcq'),
(5,'Most electronegative element is','oxygen','fluorine','chlorine','nitrogen','b',None,None,'mcq'),
(5,'Hybridization of carbon in ethene is','sp','sp2','sp3','dsp2','b',None,None,'mcq'),
(5,'SI unit of molar concentration','mol','mol/L','g/L','kg','b',None,None,'mcq'),
(5,'Reducing agent undergoes','oxidation','reduction','neutralization','hydrolysis','a',None,None,'mcq'),
(5,'Gas law PV = constant at constant T is','charles law','boyles law','avogadro law','ideal law','b',None,None,'mcq'),
(5,'Strong base among following is','NH4OH','NaOH','Al(OH)3','Mg(OH)2','b',None,None,'mcq'),
(5,'Rusting of iron requires','oxygen','water','both','none','c',None,None,'mcq'),
(5,'IUPAC name of CH4','methane','ethane','methene','methyl','a',None,None,'mcq'),
(5,'Number of periods in periodic table','7','8','18','32','a',None,None,'mcq'),
(5,'Covalent bond is formed by','transfer of electrons','sharing of electrons','loss of electrons','gain of electrons','b',None,None,'mcq'),
(5,'p-block elements lie between groups','1-2','3-12','13-18','17-18','c',None,None,'mcq'),
(5,'Oxidation number of Na in NaCl is','+1','-1','0','+2','a',None,None,'mcq'),
(5,'Catalyst affects','equilibrium','rate of reaction','enthalpy','entropy','b',None,None,'mcq'),
(5,'Functional group of aldehyde is','-COOH','-CHO','-OH','-NH2','b',None,None,'mcq'),
(5,'Hard water contains','Na salts','Ca and Mg salts','K salts','Fe salts','b',None,None,'mcq'),
(5,'Electrolysis is process of','oxidation','reduction','redox','neutralization','c',None,None,'mcq'),
(5,'Atomic radius decreases across period due to','shielding','nuclear charge','mass','neutrons','b',None,None,'mcq'),
(5,'H2SO4 is called','hydrochloric acid','sulphuric acid','nitric acid','carbonic acid','b',None,None,'mcq'),

# ---------- Integer (5) ----------
(5,'Atomic number of nitrogen','None','None','None','None',None,7,None,'integer'),
(5,'Number of valence electrons in oxygen','None','None','None','None',None,6,None,'integer'),
(5,'pH of neutral solution','None','None','None','None',None,7,None,'integer'),
(5,'Number of atoms in CO2 molecule','None','None','None','None',None,3,None,'integer'),
(5,'Molar mass of oxygen','None','None','None','None',None,16,None,'integer'),

## ------------- QUIZ-7---------------------##
# ---------- MCQs (20) ----------
(7,'Which is a noble gas','oxygen','nitrogen','neon','hydrogen','c',None,None,'mcq'),
(7,'Bond angle in methane is','90°','109.5°','120°','180°','b',None,None,'mcq'),
(7,'Which compound shows hydrogen bonding','H2O','CH4','CO2','H2','a',None,None,'mcq'),
(7,'Atomic mass unit is based on','H atom','C-12','O atom','N atom','b',None,None,'mcq'),
(7,'Oxidation state of oxygen in H2O2 is','-2','-1','0','+1','b',None,None,'mcq'),
(7,'Which acid is present in vinegar','formic','acetic','citric','lactic','b',None,None,'mcq'),
(7,'Electrolytes conduct electricity in','solid state','liquid state','gaseous state','vacuum','b',None,None,'mcq'),
(7,'Periodic table arranged by','atomic mass','atomic number','valency','density','b',None,None,'mcq'),
(7,'Which element is liquid at room temperature','iron','bromine','iodine','chlorine','b',None,None,'mcq'),
(7,'pH scale ranges from','0–7','1–7','0–14','1–14','c',None,None,'mcq'),
(7,'Strongest intermolecular force','dipole','hydrogen bond','van der waals','ionic','b',None,None,'mcq'),
(7,'Common salt chemical formula','NaCl','KCl','Na2CO3','CaCl2','a',None,None,'mcq'),
(7,'Gas released during electrolysis of water','oxygen','hydrogen','both','none','c',None,None,'mcq'),
(7,'Functional group of carboxylic acid','-OH','-COOH','-CHO','-NH2','b',None,None,'mcq'),
(7,'Most abundant gas in atmosphere','oxygen','nitrogen','carbon dioxide','argon','b',None,None,'mcq'),
(7,'Which metal is extracted by electrolysis','iron','aluminium','copper','zinc','b',None,None,'mcq'),
(7,'Allotrope of carbon is','diamond','coal','petroleum','graphite','a',None,None,'mcq'),
(7,'Avogadro number value is','6.02×10^23','3×10^8','1.6×10^-19','9.8','a',None,None,'mcq'),
(7,'Which has highest boiling point','NH3','H2O','CH4','H2','b',None,None,'mcq'),
(7,'Rate of reaction increases with','decrease in temperature','increase in surface area','decrease in pressure','absence of catalyst','b',None,None,'mcq'),

# ---------- Integer (5) ----------
(7,'Atomic number of carbon','None','None','None','None',None,6,None,'integer'),
(7,'Number of neutrons in C-12','None','None','None','None',None,6,None,'integer'),
(7,'Number of periods in periodic table','None','None','None','None',None,7,None,'integer'),
(7,'Valency of oxygen','None','None','None','None',None,2,None,'integer'),
(7,'pH of pure water at 25°C','None','None','None','None',None,7,None,'integer'),

## ------------- QUIZ-9---------------------##
# ---------- MCQs (20) ----------
(9,'Derivative of sin x is','cos x','-cos x','sin x','-sin x','a',None,None,'mcq'),
(9,'Value of cos 0°','0','1','-1','undefined','b',None,None,'mcq'),
(9,'Degree of polynomial 3x⁴ + 2','1','2','3','4','d',None,None,'mcq'),
(9,'Integral of 0 dx is','0','1','x','c','a',None,None,'mcq'),
(9,'If a matrix has 2 rows and 3 columns, its order is','2×3','3×2','2×2','3×3','a',None,None,'mcq'),
(9,'Sum of roots of quadratic ax²+bx+c=0','c/a','b/a','-b/a','-c/a','c',None,None,'mcq'),
(9,'Slope of y = mx + c is','c','m','y','x','b',None,None,'mcq'),
(9,'Value of tan 45°','0','1','√3','∞','b',None,None,'mcq'),
(9,'Mean of first n natural numbers','n/2','(n+1)/2','n','n+1','b',None,None,'mcq'),
(9,'Distance between (0,0) and (3,4)','5','4','3','7','a',None,None,'mcq'),
(9,'Determinant of [[1,0],[0,1]]','0','1','2','-1','b',None,None,'mcq'),
(9,'If sin θ = 0, θ =','0°','90°','180°','both a and c','d',None,None,'mcq'),
(9,'Log₁₀100 equals','1','2','10','100','b',None,None,'mcq'),
(9,'Area of triangle with base b and height h','bh','½bh','2bh','b+h','b',None,None,'mcq'),
(9,'Number of solutions of x² = 9','1','2','3','0','b',None,None,'mcq'),
(9,'Value of |−8|','-8','0','8','1','c',None,None,'mcq'),
(9,'If A ∪ B = A, then B is','subset of A','superset of A','equal to A','disjoint','a',None,None,'mcq'),
(9,'Equation of x-axis is','x=0','y=0','x=y','y=x','b',None,None,'mcq'),
(9,'Trigonometric identity','sin²θ+cos²θ=1','sinθ+cosθ=1','tanθ=1','cosθ=0','a',None,None,'mcq'),
(9,'If determinant is zero, matrix is','invertible','singular','identity','diagonal','b',None,None,'mcq'),

# ---------- Integer (5) ----------
(9,'Value of 7²','None','None','None','None',None,49,None,'integer'),
(9,'Degree of polynomial x³ + 5','None','None','None','None',None,3,None,'integer'),
(9,'Value of sin 90°','None','None','None','None',None,1,None,'integer'),
(9,'Number of sides of hexagon','None','None','None','None',None,6,None,'integer'),
(9,'Value of π (nearest integer)','None','None','None','None',None,3,None,'integer'),
## ------------- QUIZ-8---------------------##
# ---------- MCQs (20) ----------
(8,'Derivative of x³','3x²','x²','3x','x³','a',None,None,'mcq'),
(8,'Value of sin 0°','0','1','-1','undefined','a',None,None,'mcq'),
(8,'Sum of angles of quadrilateral','180°','270°','360°','90°','c',None,None,'mcq'),
(8,'Value of log₁₀1','0','1','10','∞','a',None,None,'mcq'),
(8,'Integral of 1 dx','1','x','0','x²','b',None,None,'mcq'),
(8,'Slope of vertical line is','0','1','undefined','infinite','c',None,None,'mcq'),
(8,'Distance formula in 2D','√(x²+y²)','√((x₂−x₁)²+(y₂−y₁)²)','|x−y|','x+y','b',None,None,'mcq'),
(8,'Roots of x²−4=0','±1','±2','4','0','b',None,None,'mcq'),
(8,'Value of tan 0°','0','1','∞','-1','a',None,None,'mcq'),
(8,'Median of 1,3,5','1','3','5','4','b',None,None,'mcq'),
(8,'Determinant of zero matrix','0','1','undefined','infinite','a',None,None,'mcq'),
(8,'If cos θ = 1, θ =','0°','90°','180°','360°','a',None,None,'mcq'),
(8,'Area of circle formula','2πr','πr²','πd','r²','b',None,None,'mcq'),
(8,'If a=b, then a−b =','1','0','b','a','b',None,None,'mcq'),
(8,'Number of diagonals in square','2','3','4','5','a',None,None,'mcq'),
(8,'Inverse of identity matrix is','zero','identity','transpose','undefined','b',None,None,'mcq'),
(8,'Probability lies between','0 and 1','1 and 2','-1 and 1','0 only','a',None,None,'mcq'),
(8,'Equation of y-axis','x=0','y=0','x=y','y=x','a',None,None,'mcq'),
(8,'If |x|=5, x equals','5','-5','±5','0','c',None,None,'mcq'),
(8,'Value of cos 60°','0','1','1/2','√3/2','c',None,None,'mcq'),

# ---------- Integer (5) ----------
(8,'Value of 9²','None','None','None','None',None,81,None,'integer'),
(8,'Number of solutions of x²=0','None','None','None','None',None,1,None,'integer'),
(8,'Degree of polynomial 5','None','None','None','None',None,0,None,'integer'),
(8,'Value of tan 45°','None','None','None','None',None,1,None,'integer'),
(8,'Number of sides of triangle','None','None','None','None',None,3,None,'integer')
]





cursor.executemany(
    """
    INSERT OR IGNORE INTO questions
    (quiz_id, question_text, option_a, option_b, option_c, option_d,
     correct_option, integer_answer, image_path, question_type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    questions
)

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_quiz_attempts (
               attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               quiz_id INTEGER NOT NULL,
               score INTEGER NOT NULL,
               total_marks INTEGER NOT NULL,
               total_questions INTEGER NOT NULL,
               correct_questions INTEGER NOT NULL,
               incorrect_questions INTEGER NOT NULL,
               unattempted_questions INTEGER NOT NULL,
               attempted_questions INTEGER NOT NULL,
               accuracy REAL NOT NULL,
               FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE,
               FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")
cursor.execute("""
    INSERT OR IGNORE INTO users (username, password, name, role) VALUES
('user01', 'pass123', 'Aarav Sharma', 'user'),
('user02', 'pass123', 'Rohan Verma', 'user'),
('user03', 'pass123', 'Ananya Gupta', 'user'),
('user04', 'pass123', 'Kunal Mehta', 'user'),
('user05', 'pass123', 'Priya Singh', 'user'),
('user06', 'pass123', 'Aditya Jain', 'user'),
('user07', 'pass123', 'Sneha Kapoor', 'user'),
('user08', 'pass123', 'Vikram Malhotra', 'user'),
('user09', 'pass123', 'Neha Agarwal', 'user'),
('user10', 'pass123', 'Rahul Khanna', 'user'),
('user11', 'pass123', 'Ishita Arora', 'user'),
('user12', 'pass123', 'Siddharth Roy', 'user'),
('user13', 'pass123', 'Pooja Nair', 'user'),
('user14', 'pass123', 'Mohit Bansal', 'user'),
('user15', 'pass123', 'Aditi Chawla', 'user'),
('user16', 'pass123', 'Nikhil Saxena', 'user'),
('user17', 'pass123', 'Kritika Joshi', 'user'),
('user18', 'pass123', 'Varun Patel', 'user'),
('user19', 'pass123', 'Simran Kaur', 'user'),
('user20', 'pass123', 'Yash Tiwari', 'user');
""")

cursor.execute("""INSERT INTO user_quiz_attempts (
    user_id,
    quiz_id,
    score,
    total_marks,
    total_questions,
    correct_questions,
    incorrect_questions,
    unattempted_questions,
    attempted_questions,
    accuracy
) VALUES
(1, 1, 88, 100, 25, 22, 3, 0, 25, 88.00),
(2, 1, 76, 100, 25, 19, 4, 2, 23, 82.61),
(3, 1, 92, 100, 25, 23, 2, 0, 25, 92.00),
(4, 1, 64, 100, 25, 16, 6, 3, 22, 72.73),
(5, 1, 70, 100, 25, 18, 5, 2, 23, 78.26),

(6, 2, 85, 100, 25, 21, 3, 1, 24, 87.50),
(7, 2, 78, 100, 25, 19, 5, 1, 24, 79.17),
(8, 2, 90, 100, 25, 23, 2, 0, 25, 92.00),
(9, 2, 66, 100, 25, 17, 6, 2, 23, 73.91),
(10, 2, 72, 100, 25, 18, 5, 2, 23, 78.26),

(11, 3, 80, 100, 25, 20, 4, 1, 24, 83.33),
(12, 3, 88, 100, 25, 22, 3, 0, 25, 88.00),
(13, 3, 74, 100, 25, 18, 5, 2, 23, 78.26),
(14, 3, 69, 100, 25, 17, 6, 2, 23, 73.91),
(15, 3, 95, 100, 25, 24, 1, 0, 25, 96.00),

(16, 1, 82, 100, 25, 20, 4, 1, 24, 83.33),
(17, 2, 88, 100, 25, 22, 3, 0, 25, 88.00),
(18, 3, 76, 100, 25, 19, 4, 2, 23, 82.61),
(19, 1, 68, 100, 25, 17, 6, 2, 23, 73.91),
(20, 2, 91, 100, 25, 23, 2, 0, 25, 92.00);
""")




  
conn.commit()
conn.close()
print("DATABASE")