"""
Gebrauchsanweisung :)

Wenn du die Selektion der OSM-Elemente verändern willst
(zB ein weiteres Tag hinzufügen oder auf eine Region beschränken):
ändere die Anfrage in der Funktion getdata().

Wenn du ändern willst, welche Informationen über das Element in der Karte angezeigt werden
(zB die Adresse hinzufügen):
ändere das in der Funktion makelist.

Wenn du die Inhalte der HTML-Datei ausserhalb der OSM-Elemente verändern willst:
ändere das in der Funktion printhtml.

"""

import overpy
import re
import phonenumbers

# gibt alle OSM-Elemente zurück, die die entsprechenden Tags haben.
def getdata():
    api = overpy.Overpass()
    
    # Overpass QL Anfrage (Anfragesprache für OSM) sucht in ganz Deutschland
    # Es kann gesucht werden nach: node, way, relation, nwr, nw, wr, nr und area
    result = api.query(
        """[out:json][timeout:60];
        area[name="Deutschland"]->.de; 
        area.de->.searchArea;
        (
        node
            [~"^product.*"~".*viez.*"]
            (area.searchArea);
        node
            [~"^vending.*"~".*viez.*"]
            (area.searchArea);
        node
            ["drink:viez"="served"]
            (area.searchArea);
        node
            ["craft"="fruit press"]
            (area.searchArea);
        node
            [~"^description.*"~".*Viez.*"]
            (area.searchArea);
        way
            ["site_type"="industrial"]
            (area.searchArea);
        way
            [~"^description.*"~".*Viez.*"]
            (area.searchArea);
        way
            [~"^product.*"~".*viez.*"]
            (area.searchArea);
        );
        out;
        >;
        out skel qt;"""
        )
    nodes = set(result.get_nodes())
    print("Anzahl nodes: ",len(nodes)) # Gibt die Gesamtzahl der Punkte zurück
    ways = set(result.get_ways())
    print("Anzahl ways: ", len(ways))
    return(nodes, ways)
    
def makelist(data):
    node_data = data[0]
    way_data = data[1]
    """bettet die relevanten Inhalte der OSM-Elemente in HTML-Zeilen ein"""
    li = "" # String für die Marker-Definition
    gl = "" # String für die Gruppierung der Gastronomien
    vm = "" # String für die Gruppierung der Automaten
    kl = "" # String für die Gruppierung der Keltereien
    sw = "" # String für die Gruppierung von Sehenswürdigkeiten, wie bspw. Museen und römische Kelteranlagen
    vs = "" # String für die Gruppierung der Viezstrassenmitglieder
    vk = "" # String für die Gruppierung von Verkaufsstellen
    ev = "" # String für die Gruppierung von Vereinen
    vereine = []
    gastro = [] 
    vending_machine = []
    keltereien = []
    sehenswuerdigkeiten = []
    viezstrasse = []
    verkaufsstellen = []

    for node in node_data: 
        if "name" in node.tags:
            var_name = re.sub('[^A-Za-z0-9]+', '', node.tags['name'].lower())   # erzeugt Variablennamen für die spätere Zuordnung zu Layern
            if "addr:city" in node.tags:
               var_name += re.sub('[^A-Za-z0-9]+', '', node.tags['addr:city'].lower())
            if "amenity" in node.tags: #Überprüfe, ob es ne Gastro ist
                if node.tags['amenity'] == 'vending_machine': # überprüfen, ob es ein Viez-Automat ist
                    vending_machine.append(var_name)
                    li += "var " + var_name + " = L.marker({lon: %s, lat: %s}, {icon: vending_machine}).bindPopup('%s');\n" % (node.lon, node.lat, make_popuptext(node))
                elif "drink:viez" in node.tags:
                    new_var_name = "gastro_"+ var_name
                    gastro.append(new_var_name)
                    li += "var " + new_var_name + " = L.marker({lon: %s, lat: %s}, {icon: gastro}).bindPopup('%s');\n" % (node.lon, node.lat, make_popuptext(node, 'gastro'))
            if "product" in node.tags: # überprüfe ob es eine Verkaufsstelle für Viez ist
                if "craft" in node.tags: 
                    if node.tags["craft"] in ["fruit press", "winery", "juice_press", "distillery"]: #überprüfe, ob es eine Kelteranlage ist
                        new_var_name = 'kt_' + var_name
                        keltereien.append(new_var_name)
                        li += "var " + new_var_name + " = L.marker({lon: %s, lat: %s}, {icon: kelterei}).bindPopup('%s');\n" % (node.lon, node.lat, make_popuptext(node))
                else:
                    verkaufsstellen.append(var_name)
                    li += "var " + var_name + " = L.marker({lon: %s, lat: %s}, {icon: verkaufsstelle}).bindPopup('%s');\n" % (node.lon, node.lat, make_popuptext(node))
            if "description" in node.tags:
                if "Viezstraße" in node.tags["description"]:
                    new_var_name = 'vs_'+ var_name
                    viezstrasse.append(new_var_name)
                    li += "var " + new_var_name + " = L.marker({lon: %s, lat: %s}, {icon: viezstrasse}).bindPopup('%s');\n" % (node.lon, node.lat, make_popuptext(node))
                if "Verein" in node.tags["description"]:
                    new_var_name = 'ev_'+ var_name
                    vereine.append(new_var_name)
                    li += "var " + new_var_name + " = L.marker({lon: %s, lat: %s}, {icon: verein}).bindPopup('%s');\n" % (node.lon, node.lat, make_popuptext(node))
            if "e.V." in node.tags["name"]:
                new_var_name = 'ev_'+ var_name
                if new_var_name not in vereine:
                    vereine.append(new_var_name)
                    li += "var " + new_var_name + " = L.marker({lon: %s, lat: %s}, {icon: verein}).bindPopup('%s');\n" % (node.lon, node.lat, make_popuptext(node))
            if "tourism" in node.tags:
                if "attraction" in node.tags["tourism"] or "museum" in node.tags["tourism"]:
                    li += "var " + var_name + " = L.marker({lon: %s, lat: %s}, {icon: sehenswuerdigkeit}).bindPopup('%s');\n" % (node.lon, node.lat, make_popuptext(node))
                    sehenswuerdigkeiten.append(var_name)
                

    markers_array = ['uni_trier']
    markers_array.extend(gastro)
    markers_array.extend(vending_machine)
    markers_array.extend(keltereien)
    markers_array.extend(viezstrasse)
    markers_array.extend(verkaufsstellen)
    markers_array.extend(vereine)
    markers_array.extend(sehenswuerdigkeiten)  
    
    count = 1 # hiermit werden die Variablennamen nummeriert
    fn = "" # String für das Zeichnen der Linien pro Flaeche
    flaechen = "" # String fuer die Erstellung der Koordinatenlisten pro Flaeche
    for way in way_data: # zeichnet Flaechen 
        if "name" in way.tags:
            nodes = way.get_nodes()
            #print(way.tags['name'])
            var_name = re.sub('[^A-Za-z0-9]+', '', way.tags['name'].lower())
            if "addr:city" in way.tags:
                var_name += re.sub('[^A-Za-z0-9]+', '', way.tags['addr:city'].lower()) # erzeugt Variablennamen für die spätere Zuordnung zu Layern
            if "product" in way.tags: # überprüfe ob es eine Verkaufsstelle für Viez ist
                print("product ", way.tags['name'])
                if "craft" in way.tags: 
                    if way.tags["craft"] in ["fruit press", "winery", "juice_press", "distillery"]: #überprüfe, ob es eine Kelteranlage ist
                        new_var_name = 'kt_' + var_name
                        if new_var_name not in keltereien:
                            keltereien.append(new_var_name)
                            markers_array.append(new_var_name)
                            li += "var " + new_var_name + " = L.marker({lon: %s, lat: %s}, {icon: kelterei}).bindPopup('%s');\n" % (nodes[0].lon, nodes[0].lat, make_popuptext(way))
                        line = draw_lines(nodes, keltereien, new_var_name + str(count))
                        flaechen += line[0]
                        fn += line[1]
                else:
                    print("verkaufsstellen ", way.tags['name'])
                    if var_name not in verkaufsstellen:
                        verkaufsstellen.append(var_name)
                        markers_array.append(var_name)
                        li += "var " + var_name + " = L.marker({lon: %s, lat: %s}, {icon: verkaufsstelle}).bindPopup('%s');\n" % (nodes[0].lon, nodes[0].lat, make_popuptext(way))
                    line = draw_lines(nodes, verkaufsstellen, new_var_name + str(count))
                    flaechen += line[0]
                    fn += line[1]
            if "description" in way.tags:
                if "Viezstraße" in way.tags["description"]:
                    new_var_name = 'vs_'+ var_name
                    if new_var_name not in viezstrasse:
                        viezstrasse.append(new_var_name)
                        markers_array.append(new_var_name)
                        li += "var " + new_var_name + " = L.marker({lon: %s, lat: %s}, {icon: viezstrasse}).bindPopup('%s');\n" % (nodes[0].lon, nodes[0].lat, make_popuptext(way))
                    line = draw_lines(nodes, viezstrasse, new_var_name + str(count))
                    flaechen += line[0]
                    fn += line[1]
            if "tourism" in way.tags:
                if "attraction" in way.tags["tourism"] or "museum" in way.tags["tourism"]:
                    li += "var " + var_name + " = L.marker({lon: %s, lat: %s}, {icon: sehenswuerdigkeit}).bindPopup('%s');\n" % (nodes[0].lon, nodes[0].lat, make_popuptext(way)) # bindet das Popup an die erste Node
                    sehenswuerdigkeiten.append(var_name)
                    markers_array.append(var_name)
                    line = draw_lines(nodes, sehenswuerdigkeiten, var_name + str(count))
                    flaechen += line[0]
                    fn += line[1]
            if "historic" in way.tags:
                if "archaeological_site" in way.tags["historic"]:
                    if var_name not in sehenswuerdigkeiten:
                        li += "var " + var_name + " = L.marker({lon: %s, lat: %s}, {icon: sehenswuerdigkeit}).bindPopup('%s');\n" % (nodes[0].lon, nodes[0].lat, make_popuptext(way))
                        sehenswuerdigkeiten.append(var_name)
                        markers_array.append(var_name)
                        line = draw_lines(nodes, sehenswuerdigkeiten, var_name + str(count))
                        flaechen += line[0]
                        fn += line[1]
            count += 1
          

    str_g =  str(gastro).replace("'","")  
    str_vm = str(vending_machine).replace("'","")
    str_k = str(keltereien).replace("'","")
    str_sw = str(sehenswuerdigkeiten).replace("'","")
    str_mv = str(viezstrasse).replace("'","")
    str_vs = str(verkaufsstellen).replace("'","")
    str_ev = str(vereine).replace("'","")
    
    
    print(len(markers_array))
    markers = "var markers = " + str(markers_array).replace("'","")
    
    gl += "var gastro = L.layerGroup(%s);" % str_g # die Anführungszeichen müssen entfernt werden
    vm += "var vending_machine = L.layerGroup(%s);" % str_vm
    kl += "var keltereien = L.layerGroup(%s);" % str_k
    sw += "var sehenswuerdigkeiten = L.layerGroup(%s);" % str_sw
    vs += "var mitglieder_viezstrasse = L.layerGroup(%s);" % str_mv
    vk += "var verkaufsstellen = L.layerGroup(%s);" % str_vs
    ev += "var vereine = L.layerGroup(%s);" % str_ev
    
        
    return li, gl, vm, kl, sw, vs, vk, ev, flaechen, fn, markers
    
    
def draw_lines(nodes, group, name):
    """Zeichnet die Flächen in die Karte ein"""
    flaeche = [] # der array mit den Nodes die zu einem Bauwerk gehören
    var_f_name = "flaeche_" + name
    fn_name = "line_" + name
    for node in nodes:
        flaeche.append([float(node.lat),float(node.lon)])
    fl = "var " + var_f_name + " = " +str(flaeche) + ";\n"
    fn = "var " + fn_name + "= L.polyline(%s, {color: 'red'});\n" % (var_f_name)
    group.append(fn_name)
    
    return fl, fn
    
def make_html_string(string):
    """Wandelt einen regulären String mit Sonderzeichen in einen HTML-Konformen String um"""
    sonderzeichen = [('Ä', '&Auml;'),('Ü', '&Uuml;'),('Ö', '&Ouml;'),('ä', '&auml;'),('ö', '&ouml;'),('ü', '&uuml;'),('ß','&szlig;'),('é', '&eacute;')]
    for tupel in sonderzeichen:
        string = string.replace(tupel[0],tupel[1])
   # print(string)
    return string

def translate_string(string):
    """Ersetzt englische Bezeichnungen durch deutsche"""
    if string == 'cafe':
        string = 'Caf&eacute;'
    elif string == 'fast_food':
        string = 'Fast Food'
    elif string == 'food_court':
        string = 'Schlemmermeile'
    elif string == 'ice_cream':
        string = 'Eisdiele'
    elif string == 'cinema':
        string = 'Kino'
    elif string == 'nightclub':
        string = 'Nachtclub'
    elif string == 'social_centre':
        string = 'Soziales Zentrum'
    elif string == 'theatre':
        string = 'Theater'
    else: string = string.capitalize()
    return string
    
def standardize_phone(phone):
    """Wandelt alle Telefonnummer in ein einheitliches internationales Format der Form +49 xxx xxxx oder +49 xxxx xxxx um"""
    if ';' in phone:
        numbers = phone.split(';') 
        phone = numbers[0]
    number = phonenumbers.parse(phone, "DE")
    international_phone = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return(international_phone)
    
def make_popuptext(node, category = ""):
    """Erzeugt den Text für die einzelnen Popups"""
    category = category
    kategoriename = ""
    website = ""
    strasse = ""
    ort = ""
    phone = ""
    email = ""
    if "'" in node.tags['name']:
       node.tags['name'] = node.tags['name'].replace("'", "\\'")
    if category == "gastro":
        kategoriename += "<br>" + translate_string(node.tags['amenity'])
    if "website" in node.tags:
        website += '<a href ="' + node.tags['website'] + '" target = "_blank"><img src= "assets/bootstrap-icons/box-arrow-up-right.svg" alt = "Zur Webseite" height = "12px" width = "auto">Zur Webseite</a>'
    if "addr:street" in node.tags:
        strasse += "<br>" + node.tags['addr:street']
    if "addr:housenumber" in node.tags:
        if strasse != "":
         strasse += " "
        strasse += node.tags['addr:housenumber']
    if "addr:postcode" in node.tags: 
        ort +=  '<br>' + node.tags['addr:postcode']
    if "addr:city" in node.tags:
        if ort != "":
            ort += " "
        ort += node.tags['addr:city']
    adresse = make_html_string(strasse) + make_html_string(ort)
    if 'phone' in node.tags:
        phone += '<br><img src="assets/bootstrap-icons/telephone-fill.svg" class = "popup" alt = "Telefon">' + standardize_phone(node.tags['phone'])
    if 'email' in node.tags:
       # print(node.tags['email'])
        email += '<a href="mailto:' + node.tags['email'] + '"><img src= "assets/bootstrap-icons/envelope-fill.svg" class = "popup" alt = "E-Mail"> E-Mail</a><br>'
    popuptext = "<p><b>%s</b>%s%s%s<br>%s%s</p>" % (make_html_string(node.tags['name']), kategoriename, adresse, phone, email, website)
    return popuptext
    
def printhtml(arguments):
    """druckt den gesamten HTML-Inhalt, OSM-Elemente werden eingefügt"""
    li = arguments[0]
    gl = arguments[1]
    vm = arguments[2]
    kl = arguments[3]
    sw = arguments[4]
    vs = arguments[5]
    vk = arguments[6]
    ev = arguments[7]
    flaechen = arguments[8]
    fn = arguments[9]
    markers = arguments[10]
    string = """
    <!DOCTYPE HTML>
<html lang="de">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/OverlappingMarkerSpiderfier-Leaflet/0.2.6/oms.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <link rel="stylesheet" href="viezkarte.css" />
  </head>
  <body>
    <div id="map"></div>
  <script>
  
    var digital_viez = L.icon({
    iconUrl: 'assets/map-icons/projekt-icon.png',
    iconSize: [50, 50],
    iconAnchor: [25, 25],
    popupAnchor: [5, -20],
});	
    var organisationen = L.icon({
    iconUrl: 'assets/map-icons/vereine-icon.png',
    iconSize: [50, 50],
    iconAnchor: [25, 25],
    popupAnchor: [5, -20],
});
	var gastro = L.icon({
    iconUrl: 'assets/map-icons/gastro-icon.png',
    iconSize: [50, 50],
    iconAnchor: [25, 25],
    popupAnchor: [5, -20],
});
	var kelterei = L.icon({
    iconUrl: 'assets/map-icons/hersteller-icon.png',
    iconSize: [50, 50],
    iconAnchor: [25, 25],
    popupAnchor: [5, -20],
});

	var vending_machine = L.icon({
    iconUrl: 'assets/map-icons/automaten-icon.png',
    iconSize: [50, 50],
    iconAnchor: [25, 25],
    popupAnchor: [5, -20],
});

var sehenswuerdigkeit = L.icon({
    iconUrl: 'assets/map-icons/attraktionen-icon.png',
    iconSize: [50, 50],
    iconAnchor: [25, 25],
    popupAnchor: [5, -20],
});

var viezstrasse = L.icon({
    iconUrl: 'assets/map-icons/viezstrasse-icon.png',
    iconSize: [50, 50],
    iconAnchor: [25, 25],
    popupAnchor: [5, -20],
});

var verkaufsstelle = L.icon({
    iconUrl: 'assets/map-icons/verkauf-icon.png',
    iconSize: [50, 50],
    iconAnchor: [25, 25],
    popupAnchor: [5, -20],
});

var verein = L.icon({
    iconUrl: 'assets/map-icons/vereine-icon.png',
    iconSize: [50, 50],
    iconAnchor: [25, 25],
    popupAnchor: [5, -20],
});

var latlngs = [
	[49.7520346, 6.6328894], <!-- Anfang Viezstrasse in Trier, Seitenstrasse an der Lorenz-Kellner-Strasse -->
	[49.7518714, 6.6326308], <!-- Knick in der Seitenstrasse der Lorenz-Kellner-Strasse -->
	[49.7518196, 6.6325913], <!-- Seitenstrasse an der Lorenz-Kellner-Strasse -->
	[49.7520582, 6.6321099], <!-- Anfang Lorenz-Kellner-Strasse -->
	[49.7509633, 6.6315218], <!-- Ende Lorenz-Kellner-Strasse -->
	[49.7508865, 6.6314816], <!-- Kreuzung Lorenz-Kellner-Strasse und Kaiserstrasse -->
	[49.7511561, 6.6295155], <!-- Mitte Kaiserstrasse an Kreuzung Wallstrasse -->
	[49.7512986, 6.6284324], <!-- Knick Kaiserstrasse -->
	[49.7512972, 6.6283740], <!-- Ende Kaiserstrasse -->
	[49.7512446, 6.6281402], <!-- Johanniterufer/St. Barbara-Ufer -->
	[49.7511004, 6.6281039], <!-- St. Barbara-Ufer Abknick Suedallee -->
	[49.7509310, 6.6280630], <!-- St. Barbara-Ufer Fussgaengeruebergang -->
	[49.7505522, 6.6279829], <!-- St. Barbara-Ufer Verlauf --> 
	[49.7495781, 6.6277843], <!-- St. Barbara-Ufer in der Naehe zur Gilberstrasse -->
	[49.7485512, 6.6277026], <!-- St. Barbara-Ufer in der Naehe zur Sporthalle -->
	[49.7478639, 6.6277424], <!-- St. Barbara-Ufer Verlauf -->
	[49.7470437, 6.6278287], <!-- St. Barbara-Ufer Naehe Feuerwehr -->
	[49.7464026, 6.6278977], <!-- St. Barbara-Ufer Kreuzung Saarbruecker Strasse -->
	[49.7461318, 6.6279268], <!-- St. Barbara-Ufer Naehe Shell-Select Tankstelle -->
	[49.7447787, 6.6280656], <!-- St. Barbara-Ufer Uebergang Paceliufer -->
	[49.7429235, 6.6283744], <!-- Paceliufer/Anfang Toepferstrasse -->
	<!-- Geokoordinaten von der Viezstrassen-Seite ab hier -->
	[49.742822, 6.629311],
	[49.742346, 6.631267],
	[49.740181, 6.630425],
	[49.740181, 6.630425],
	[49.73961, 6.631748],
	[49.73736, 6.629997],
	[49.734897, 6.628443],
	[49.731517, 6.628071],
	[49.73072, 6.62847],
	[49.730559, 6.628323],
	[49.730343, 6.627678],
	[49.730023, 6.627604],
	[49.729589, 6.626964],
	[49.729302, 6.626829],
	[49.728649, 6.627106],
	[49.728649, 6.627106],
	[49.727788, 6.626935],
	[49.725974, 6.627227],
	[49.725239, 6.627522],
	[49.724575, 6.628217],
	[49.723811, 6.629343],
	[49.72305, 6.62983],
	[49.722486, 6.629819],
	[49.720006, 6.629128],
	[49.718606, 6.627683],
	[49.718101, 6.627497],
	[49.717736, 6.627739],
	[49.717736, 6.627739],
	[49.71668, 6.628932],
	[49.71597, 6.629301],
	[49.715372, 6.630267],
	[49.7149, 6.63062],
	[49.713975, 6.630621],
	[49.712268, 6.629932],
	[49.711235, 6.630599],
	[49.710931, 6.630636],
	[49.709051, 6.628876],
	[49.708938, 6.628534],
	[49.708679, 6.62825],
	[49.707174, 6.6269],
	[49.707174, 6.6269],
	[49.705598, 6.625188],
	[49.703783, 6.622292],
	[49.701501, 6.619758],
	[49.699012, 6.617256],
	[49.697483, 6.616281],
	[49.696699, 6.615284],
	[49.696699, 6.615284],
	[49.696132, 6.613801],
	[49.69598, 6.613706],
	[49.695805, 6.613822],
	[49.695578, 6.614343],
	[49.695419, 6.616471],
	[49.695465, 6.617625],
	[49.695803, 6.619644],
	[49.695847, 6.622887],
	[49.695065, 6.62686],
	[49.694812, 6.627408],
	[49.694606, 6.62757],
	[49.693594, 6.627044],
	[49.693594, 6.627044],
	[49.693237, 6.627093],
	[49.691562, 6.625068],
	[49.691119, 6.624231],
	[49.690977, 6.623661],
	[49.690994, 6.62005],
	[49.690889, 6.618766],
	[49.690285, 6.616608],
	[49.689617, 6.613422],
	[49.689113, 6.611998],
	[49.68901, 6.611164],
	[49.68901, 6.611164],
	[49.689562, 6.607253],
	[49.689501, 6.604125],
	[49.689657, 6.601793],
	[49.689579, 6.598809],
	[49.689721, 6.596949],
	[49.69018, 6.594002],
	[49.69018, 6.590832],
	[49.69018, 6.590832],
	[49.691202, 6.585372],
	[49.691527, 6.584545],
	[49.69238, 6.583275],
	[49.692853, 6.581446],
	[49.693398, 6.57995],
	[49.693494, 6.579038],
	[49.693109, 6.577628],
	[49.69342, 6.576365],
	[49.694106, 6.576392],
	[49.695439, 6.576078],
	[49.695727, 6.576241],
	[49.69596, 6.576605],
	[49.696491, 6.576346],
	[49.696593, 6.576515],
	[49.696711, 6.576459],
	[49.696711, 6.576459],
	[49.698971, 6.579074],
	[49.699619, 6.579715],
	[49.698971, 6.579074],
	[49.697663, 6.577458],
	[49.697122, 6.576914],
	[49.696711, 6.576459],
	[49.696717, 6.576166],
	[49.698248, 6.574005],
	[49.699342, 6.572697],
	[49.698111, 6.570625],
	[49.698111, 6.570625],
	[49.698068, 6.56844],
	[49.697793, 6.567077],
	[49.697623, 6.566762],
	[49.695577, 6.566203],
	[49.695017, 6.565921],
	[49.694856, 6.566042],
	[49.694762, 6.565863],
	[49.694244, 6.565837],
	[49.688661, 6.564294],
	[49.688501, 6.564429],
	[49.688425, 6.564254],
	[49.688425, 6.564254],
	[49.685121, 6.563368],
	[49.684907, 6.563176],
	[49.684188, 6.563127],
	[49.68117, 6.562224],
	[49.680942, 6.561813],
	[49.679926, 6.558181],
	[49.679427, 6.556915],
	[49.679655, 6.555543],
	[49.68003, 6.554561],
	[49.679758, 6.553607],
	[49.679758, 6.553607],
	[49.678606, 6.552067],
	[49.677716, 6.551526],
	[49.676179, 6.550977],
	[49.675524, 6.550253],
	[49.674882, 6.548963],
	[49.674482, 6.546545],
	[49.674322, 6.546103],
	[49.67299, 6.544172],
	[49.672065, 6.543331],
	[49.671198, 6.54203],
	[49.670865, 6.541742],
	[49.670865, 6.541742],
	[49.671025, 6.53943],
	[49.670781, 6.538112],
	[49.670813, 6.537834],
	[49.671152, 6.537117],
	[49.671321, 6.535495],
	[49.67197, 6.533423],
	[49.672456, 6.533205],
	[49.672446, 6.532259],
	[49.673005, 6.524981],
	[49.672987, 6.524579],
	[49.67283, 6.524106],
	[49.67283, 6.524106],
	[49.671394, 6.521619],
	[49.672071, 6.521234],
	[49.673343, 6.519882],
	[49.674107, 6.518509],
	[49.674192, 6.518138],
	[49.673166, 6.515933],
	[49.672658, 6.515875],
	[49.671772, 6.515042],
	[49.671459, 6.514386],
	[49.669588, 6.512629],
	[49.668759, 6.510895],
	[49.668759, 6.510895],
	[49.668145, 6.509963],
	[49.667908, 6.509273],
	[49.667474, 6.506962],
	[49.666913, 6.50272],
	[49.666709, 6.502195],
	[49.665809, 6.500867],
	[49.664787, 6.50015],
	[49.663475, 6.498662],
	[49.662251, 6.49751],
	[49.662251, 6.49751],
	[49.661776, 6.496752],
	[49.661168, 6.495202],
	[49.659545, 6.49353],
	[49.658576, 6.492931],
	[49.657564, 6.492743],
	[49.656929, 6.492465],
	[49.654436, 6.491145],
	[49.653438, 6.490453],
	[49.652014, 6.488601],
	[49.652014, 6.488601],
	[49.650556, 6.485201],
	[49.650164, 6.484665],
	[49.64801, 6.483244],
	[49.646236, 6.482997],
	[49.644887, 6.481973],
	[49.644807, 6.481694],
	[49.644385, 6.481401],
	[49.64426, 6.481594],
	[49.644621, 6.482255],
	[49.645193, 6.48392],
	[49.645577, 6.484687],
	[49.645519, 6.485182],
	[49.645348, 6.485489],
	[49.645348, 6.485489],
	[49.644183, 6.485254],
	[49.641587, 6.485109],
	[49.641459, 6.485322],
	[49.641094, 6.48687],
	[49.640415, 6.488296],
	[49.639954, 6.48836],
	[49.638785, 6.487512],
	[49.638682, 6.487574],
	[49.638646, 6.487829],
	[49.63884, 6.488783],
	[49.638712, 6.489895],
	[49.638246, 6.491871],
	[49.637888, 6.492762],
	[49.637689, 6.492994],
	[49.637689, 6.492994],
	[49.636581, 6.492805],
	[49.634205, 6.492823],
	[49.633636, 6.492857],
	[49.633488, 6.493106],
	[49.633537, 6.493408],
	[49.633862, 6.493709],
	[49.635396, 6.494808],
	[49.635676, 6.495231],
	[49.635867, 6.495897],
	[49.637291, 6.497222],
	[49.637692, 6.497988],
	[49.637421, 6.499091],
	[49.636882, 6.50043],
	[49.636615, 6.500748],
	[49.636155, 6.500839],
	[49.636155, 6.500839],
	[49.63601, 6.501012],
	[49.634762, 6.503226],
	[49.634141, 6.504685],
	[49.634282, 6.508735],
	[49.634168, 6.508986],
	[49.633796, 6.509232],
	[49.634654, 6.512656],
	[49.634776, 6.51336],
	[49.634724, 6.513682],
	[49.634015, 6.513432],
	[49.632756, 6.513364],
	[49.632756, 6.513364],
	[49.631487, 6.512706],
	[49.630436, 6.512497],
	[49.628855, 6.511313],
	[49.626581, 6.510189],
	[49.625348, 6.51035],
	[49.623286, 6.50996],
	[49.622012, 6.509914],
	[49.620322, 6.509488],
	[49.620322, 6.509488],
	[49.62047, 6.508464],
	[49.620344, 6.507811],
	[49.619211, 6.505742],
	[49.617867, 6.50442],
	[49.617494, 6.503547],
	[49.617497, 6.502753],
	[49.619148, 6.493908],
	[49.619148, 6.493908],
	[49.6193, 6.492465],
	[49.619122, 6.49146],
	[49.618567, 6.490375],
	[49.617164, 6.489801],
	[49.616907, 6.489735],
	[49.616466, 6.489904],
	[49.615468, 6.490985],
	[49.61446, 6.491091],
	[49.614221, 6.491327],
	[49.613232, 6.493206],
	[49.612402, 6.494248],
	[49.611995, 6.495513],
	[49.611978, 6.496645],
	[49.611879, 6.496996],
	[49.611879, 6.496996],
	[49.611607, 6.49685],
	[49.611376, 6.496154],
	[49.611111, 6.496166],
	[49.611108, 6.497014],
	[49.610885, 6.499003],
	[49.610385, 6.501733],
	[49.609654, 6.503335],
	[49.607334, 6.505821],
	[49.607104, 6.506236],
	[49.605626, 6.505494],
	[49.605042, 6.504814],
	[49.605042, 6.504814],
	[49.6037, 6.501243],
	[49.601922, 6.496977],
	[49.601211, 6.494054],
	[49.600726, 6.492678],
	[49.598742, 6.488459],
	[49.598742, 6.488459],
	[49.597908, 6.486987],
	[49.597758, 6.48627],
	[49.597456, 6.485849],
	[49.597202, 6.485017],
	[49.596888, 6.485077],
	[49.596565, 6.48553],
	[49.596219, 6.485729],
	[49.596109, 6.486436],
	[49.59594, 6.486595],
	[49.594694, 6.486241],
	[49.593084, 6.48686],
	[49.59249, 6.486653],
	[49.591407, 6.487173],
	[49.590063, 6.486407],
	[49.589017, 6.4876],
	[49.589017, 6.4876],
	[49.587146, 6.485351],
	[49.58526, 6.483821],
	[49.581868, 6.480425],
	[49.579221, 6.477141],
	[49.579095, 6.476952],
	[49.579061, 6.476583],
	[49.579061, 6.476583],
	[49.578441, 6.475428],
	[49.577972, 6.474845],
	[49.576958, 6.471849],
	[49.575942, 6.469624],
	[49.574574, 6.467236],
	[49.574162, 6.465096],
	[49.573743, 6.464378],
	[49.573287, 6.463942],
	[49.573199, 6.463322],
	[49.572232, 6.462447],
	[49.572232, 6.462447],
	[49.572228, 6.461907],
	[49.572812, 6.460213],
	[49.572783, 6.459696],
	[49.571525, 6.457529],
	[49.571301, 6.456235],
	[49.570922, 6.455165],
	[49.5705, 6.453018],
	[49.569966, 6.451198],
	[49.569788, 6.447552],
	[49.569393, 6.446433],
	[49.569393, 6.446433],
	[49.569813, 6.444928],
	[49.57001, 6.443762],
	[49.570724, 6.44311],
	[49.570529, 6.440585],
	[49.570832, 6.439667],
	[49.572879, 6.437402],
	[49.573989, 6.435726],
	[49.574858, 6.43466],
	[49.575372, 6.434482],
	[49.576134, 6.43477],
	[49.576511, 6.434508],
	[49.576694, 6.433999],
	[49.576694, 6.433999],
	[49.576944, 6.43208],
	[49.578024, 6.429949],
	[49.578635, 6.429128],
	[49.581109, 6.426837],
	[49.58178, 6.425863],
	[49.58284, 6.422982],
	[49.583744, 6.41913],
	[49.583744, 6.41913],
	[49.586191, 6.414762],
	[49.585718, 6.413823],
	[49.58469, 6.414143],
	[49.583569, 6.415442],
	[49.582639, 6.416139],
	[49.581449, 6.416608],
	[49.580892, 6.416615],
	[49.580549, 6.417708],
	[49.579441, 6.417572],
	[49.578768, 6.417854],
	[49.577989, 6.417944],
	[49.577675, 6.417914],
	[49.576561, 6.417329],
	[49.576561, 6.417329],
	[49.575856, 6.417743],
	[49.575713, 6.417581],
	[49.575422, 6.417961],
	[49.575432, 6.418862],
	[49.574837, 6.419929],
	[49.572506, 6.422379],
	[49.571629, 6.423033],
	[49.569773, 6.423083],
	[49.569496, 6.422922],
	[49.569287, 6.422614],
	[49.568085, 6.42027],
	[49.56776, 6.419824],
	[49.56776, 6.419824],
	[49.567122, 6.4192],
	[49.56549, 6.418064],
	[49.564592, 6.416737],
	[49.56362, 6.41566],
	[49.562758, 6.414163],
	[49.561598, 6.412762],
	[49.561093, 6.413091],
	[49.560424, 6.41292],
	[49.560155, 6.413078],
	[49.559583, 6.412984],
	[49.558185, 6.41184],
	[49.558041, 6.411596],
	[49.557874, 6.410799],
	[49.557874, 6.410799],
	[49.55673, 6.408525],
	[49.554349, 6.405782],
	[49.553669, 6.407493],
	[49.553356, 6.408743],
	[49.55341, 6.410306],
	[49.553311, 6.411928],
	[49.55309, 6.41472],
	[49.55275, 6.417181],
	[49.55275, 6.417181],
	[49.552927, 6.420081],
	[49.552903, 6.421118],
	[49.552285, 6.426862],
	[49.551553, 6.430849],
	[49.551509, 6.431789],
	[49.551629, 6.43264],
	[49.552014, 6.433799],
	[49.553055, 6.435926],
	[49.553055, 6.435926],
	[49.554397, 6.438037],
	[49.556724, 6.443506],
	[49.557244, 6.445316],
	[49.55737, 6.447308],
	[49.557297, 6.447889],
	[49.5563, 6.450093],
	[49.55627, 6.451314],
	[49.556535, 6.453041],
	[49.556512, 6.453783],
	[49.556512, 6.453783],
	[49.554483, 6.460315],
	[49.552757, 6.458272],
	[49.552186, 6.457805],
	[49.550942, 6.457378],
	[49.549335, 6.456445],
	[49.547719, 6.454282],
	[49.546955, 6.452135],
	[49.546955, 6.452135],
	[49.546145, 6.450632],
	[49.543037, 6.446306],
	[49.54152, 6.444722],
	[49.540717, 6.443639],
	[49.539148, 6.441175],
	[49.53708, 6.440069],
	[49.53639, 6.439384],
	[49.53639, 6.439384],
	[49.53432, 6.435962],
	[49.533143, 6.434463],
	[49.532343, 6.431884],
	[49.531575, 6.430966],
	[49.530879, 6.431764],
	[49.530324, 6.431489],
	[49.52984, 6.431681],
	[49.529667, 6.431974],
	[49.529144, 6.430454],
	[49.529014, 6.429529],
	[49.527341, 6.428967],
	[49.525994, 6.428082],
	[49.525994, 6.428082],
	[49.520462, 6.421206],
	[49.519349, 6.420357],
	[49.517759, 6.419719],
	[49.516624, 6.41831],
	[49.516007, 6.417906],
	[49.515391, 6.416683],
	[49.514687, 6.415888],
	[49.514585, 6.415306],
	[49.512679, 6.413328],
	[49.511769, 6.412203],
	[49.511769, 6.412203],
	[49.508076, 6.40873],
	[49.506434, 6.407918],
	[49.504975, 6.406258],
	[49.504371, 6.406094],
	[49.503701, 6.406223],
	[49.503378, 6.406537],
	[49.502903, 6.406603],
	[49.502279, 6.407268],
	[49.501428, 6.407015],
	[49.500875, 6.407422],
	[49.500588, 6.407848],
	[49.499914, 6.410803],
	[49.499943, 6.412467],
	[49.499943, 6.412467],
	[49.500271, 6.414194],
	[49.500154, 6.419372],
	[49.499779, 6.421776],
	[49.498107, 6.426315],
	[49.496682, 6.429699],
	[49.496682, 6.429699],
	[49.498368, 6.432607],
	[49.499992, 6.434818],
	[49.498583, 6.43758],
	[49.498423, 6.438443],
	[49.498222, 6.438964],
	[49.497456, 6.439085],
	[49.497065, 6.43884],
	[49.495166, 6.434753],
	[49.495164, 6.434138],
	[49.494502, 6.433265],
	[49.494445, 6.433346],
	[49.494445, 6.433346],
	[49.494326, 6.433623],
	[49.492882, 6.441997],
	[49.491666, 6.445964],
	[49.491003, 6.447265],
	[49.488769, 6.449969],
	[49.488314, 6.450747],
	[49.488314, 6.450747],
	[49.486177, 6.456248],
	[49.483, 6.463343],
	[49.482121, 6.466005],
	[49.481535, 6.467379],
	[49.480747, 6.468578],
	[49.480747, 6.468578],
	[49.479746, 6.469481],
	[49.475117, 6.472772],
	[49.473636, 6.473382],
	[49.471774, 6.473757],
	[49.471424, 6.473989],
	[49.471296, 6.47458],
	[49.471495, 6.476188],
	[49.471482, 6.47695],
	[49.471077, 6.479109],
	[49.471077, 6.479109],
	[49.471421, 6.48152],
	[49.474277, 6.488749],
	[49.476373, 6.492921],
	[49.476414, 6.493744],
	[49.475739, 6.495563],
	[49.475739, 6.495563],
	[49.476141, 6.495417],
	[49.47803, 6.494131],
	[49.478814, 6.493915],
	[49.479456, 6.494172],
	[49.480614, 6.495185],
	[49.484977, 6.49679],
	[49.485627, 6.49722],
	[49.486921, 6.49933],
	[49.486921, 6.49933],
	[49.490052, 6.501903],
	[49.491063, 6.503024],
	[49.491959, 6.504289],
	[49.492725, 6.505687],
	[49.493494, 6.507541],
	[49.494096, 6.509553],
	[49.49486, 6.512797],
	[49.495565, 6.514614],
	[49.496552, 6.516053],
	[49.496552, 6.516053],
	[49.49771, 6.517223],
	[49.498779, 6.518974],
	[49.500148, 6.520158],
	[49.500174, 6.520424],
	[49.499425, 6.521135],
	[49.496745, 6.521997],
	[49.494725, 6.521579],
	[49.49348, 6.520733],
	[49.492953, 6.520588],
	[49.492953, 6.520588],
	[49.492518, 6.520653],
	[49.491204, 6.521238],
	[49.488625, 6.521328],
	[49.488182, 6.52167],
	[49.48779, 6.522798],
	[49.487422, 6.523072],
	[49.487133, 6.522945],
	[49.486972, 6.522708],
	[49.48679, 6.521753],
	[49.486642, 6.521459],
	[49.486421, 6.521399],
	[49.486222, 6.521568],
	[49.486133, 6.522094],
	[49.486335, 6.524264],
	[49.486305, 6.524963],
	[49.485492, 6.527121],
	[49.485492, 6.527121],
	[49.485306, 6.528714],
	[49.484902, 6.530302],
	[49.48465, 6.530467],
	[49.484792, 6.532627],
	[49.484367, 6.536271],
	[49.484556, 6.537828],
	[49.483801, 6.538668],
	[49.483815, 6.53954],
	[49.484272, 6.543672],
	[49.484209, 6.544468],
	[49.483853, 6.545022],
	[49.483853, 6.545022],
	[49.483418, 6.545111],
	[49.483045, 6.544821],
	[49.482512, 6.543813],
	[49.482197, 6.543675],
	[49.481803, 6.543822],
	[49.481529, 6.544264],
	[49.481138, 6.545883],
	[49.4804, 6.547397],
	[49.479588, 6.549401],
	[49.479508, 6.550303],
	[49.479801, 6.55111],
	[49.479544, 6.551173],
	[49.479096, 6.55043],
	[49.478743, 6.550311],
	[49.47778, 6.551638],
	[49.477507, 6.551815],
	[49.477009, 6.551671],
	[49.477009, 6.551671],
	[49.475879, 6.550603],
	[49.474767, 6.550089],
	[49.474347, 6.549534],
	[49.472177, 6.550424],
	[49.471873, 6.550385],
	[49.471515, 6.549935],
	[49.471287, 6.548967],
	[49.47098, 6.548683],
	[49.46764, 6.549354],
	[49.467324, 6.549313],
	[49.466846, 6.548921],
	[49.465562, 6.548358],
	[49.465562, 6.548358],
	[49.463973, 6.546854],
	[49.462959, 6.546375],
	[49.462508, 6.545804],
	[49.461925, 6.545778],
	[49.461742, 6.545646],
	[49.461008, 6.543778],
	[49.460655, 6.54204],
	[49.45961, 6.538988],
	[49.459586, 6.534963],
	[49.459691, 6.533911],
	[49.459912, 6.533281],
	[49.459912, 6.533281],
	[49.459908, 6.532025],
	[49.459755, 6.530176],
	[49.458965, 6.526827],
	[49.457974, 6.525221],
	[49.457391, 6.524842],
	[49.456929, 6.523256],
	[49.456943, 6.52299],
	[49.457127, 6.522965],
	[49.457661, 6.524096],
	[49.457903, 6.524068],
	[49.457262, 6.51974],
	[49.457262, 6.51974],
	[49.456086, 6.517054],
	[49.453981, 6.51484],
	[49.452296, 6.518755],
	[49.451792, 6.520444],
	[49.451429, 6.521035],
	[49.45096, 6.521361],
	[49.45027, 6.521396],
	[49.44925, 6.520954],
	[49.448645, 6.520403],
	[49.448645, 6.520403],
	[49.446749, 6.518168],
	[49.446273, 6.517982],
	[49.445914, 6.518173],
	[49.445704, 6.518508],
	[49.445563, 6.519073],
	[49.445205, 6.52292],
	[49.444896, 6.523927],
	[49.443828, 6.52622],
	[49.443796, 6.526792],
	[49.443918, 6.527192],
	[49.445044, 6.529019],
	[49.445916, 6.531469],
	[49.445916, 6.531469],
	[49.446012, 6.532625],
	[49.445757, 6.53493],
	[49.445789, 6.535819],
	[49.446658, 6.53899],
	[49.447221, 6.543409],
	[49.447107, 6.545178],
	[49.446665, 6.547351],
	[49.446133, 6.548194],
	[49.446133, 6.548194],
	[49.445101, 6.548589],
	[49.444861, 6.548802],
	[49.44469, 6.549262],
	[49.444739, 6.549772],
	[49.445216, 6.550652],
	[49.448306, 6.553557],
	[49.451877, 6.559539],
	[49.451877, 6.559539],
	[49.452709, 6.560726],
	[49.454971, 6.563441],
	[49.455492, 6.564575],
	[49.456942, 6.569518],
	[49.457794, 6.571044],
	[49.458686, 6.573082],
	[49.459661, 6.574111],
	[49.46014, 6.574348],
	[49.46014, 6.574348],
	[49.462428, 6.574174],
	[49.462987, 6.574341],
	[49.464512, 6.575755],
	[49.464952, 6.576427],
	[49.465195, 6.577354],
	[49.465559, 6.579998],
	[49.466075, 6.582314],
	[49.466331, 6.582935],
	[49.467217, 6.58427],
	[49.467948, 6.585791],
	[49.467948, 6.585791],
	[49.468473, 6.587321],
	[49.468612, 6.588615],
	[49.468473, 6.589958],
	[49.468095, 6.590806],
	[49.467785, 6.591129],
	[49.466648, 6.591387],
	[49.466356, 6.591646],
	[49.466103, 6.593125],
	[49.465705, 6.593878],
	[49.465474, 6.594784],
	[49.46525, 6.59512],
	[49.464497, 6.595341],
	[49.462625, 6.595077],
	[49.461232, 6.595128],
	[49.461232, 6.595128],
	[49.460341, 6.595362],
	[49.459411, 6.595824],
	[49.458076, 6.596867],
	[49.456775, 6.597438],
	[49.456324, 6.598108],
	[49.455846, 6.599469],
	[49.455507, 6.600124],
	[49.453104, 6.602274],
	[49.452587, 6.602567],
	[49.451644, 6.602797],
	[49.451137, 6.603214],
	[49.451137, 6.603214],
	[49.449457, 6.604139],
	[49.447506, 6.605533],
	[49.445886, 6.606401],
	[49.445496, 6.606885],
	[49.444947, 6.608149],
	[49.444444, 6.608981],
	[49.441422, 6.611972],
	[49.441117, 6.612454],
	[49.440934, 6.613094],
	[49.440934, 6.613094],
	[49.440894, 6.613699],
	[49.441198, 6.617015],
	[49.43924, 6.618702],
	[49.436888, 6.620149],
	[49.435881, 6.621592],
	[49.433643, 6.623543],
	[49.433643, 6.623543],
	[49.430076, 6.627842],
	[49.42934, 6.628314],
	[49.427461, 6.629033],
	[49.425551, 6.622818],
	[49.424919, 6.619583],
	[49.424919, 6.619583],
	[49.424651, 6.618678],
	[49.422418, 6.614794],
	[49.422059, 6.613858],
	[49.421126, 6.610633],
	[49.419152, 6.607462],
	[49.417983, 6.605246],
	[49.417983, 6.605246],
	[49.417461, 6.603957],
	[49.417001, 6.60233],
	[49.416618, 6.600443],
	[49.416421, 6.598429],
	[49.416368, 6.597275],
	[49.416436, 6.595517],
	[49.416587, 6.594091],
	[49.417073, 6.591286],
	[49.418538, 6.587886],
	[49.418538, 6.587886],
	[49.421004, 6.579305],
	[49.422139, 6.574992],
	[49.42216, 6.574282],
	[49.4215, 6.572885],
	[49.421456, 6.57208],
	[49.423027, 6.568545],
	[49.423449, 6.566785],
	[49.423424, 6.565997],
	[49.423204, 6.565431],
	[49.422511, 6.564393],
	[49.422462, 6.564525],
	[49.422611, 6.564853],
	[49.422462, 6.564525],
	[49.422511, 6.564393],
	[49.422511, 6.564393],
	[49.421811, 6.563355],
	[49.41796, 6.55863],
	[49.415902, 6.552038],
	[49.415397, 6.550819],
	[49.415045, 6.550393],
	[49.414421, 6.550004],
	[49.414421, 6.550004],
	[49.412863, 6.54996],
	[49.412342, 6.549733],
	[49.411125, 6.547185],
	[49.41085, 6.545874],
	[49.410653, 6.545625],
	[49.410356, 6.545621],
	[49.408998, 6.547046],
	[49.405772, 6.549652],
	[49.405325, 6.55028],
	[49.404876, 6.551444],
	[49.404876, 6.551444],
	[49.404524, 6.552063],
	[49.402138, 6.554593],
	[49.401773, 6.555266],
	[49.400957, 6.557946],
	[49.39939, 6.560681],
	[49.398802, 6.563219],
	[49.397899, 6.564998],
	[49.397224, 6.565952],
	[49.397224, 6.565952],
	[49.396687, 6.56879],
	[49.396738, 6.569253],
	[49.397458, 6.571398],
	[49.397515, 6.574726],
	[49.397416, 6.575869],
	[49.396389, 6.581428],
	[49.396333, 6.582513],
	[49.396454, 6.584509],
	[49.396385, 6.585089],
	[49.396385, 6.585089],
	[49.394009, 6.591071],
	[49.391341, 6.599211],
	[49.389921, 6.604123],
	[49.389921, 6.604123],
	[49.389421, 6.605136],
	[49.388264, 6.606773],
	[49.387283, 6.608917],
	[49.386992, 6.609163],
	[49.385422, 6.609858],
	[49.381987, 6.612471],
	[49.381658, 6.613015],
	[49.380902, 6.614922],
	[49.380443, 6.61399],
	[49.380443, 6.61399],
	[49.378661, 6.609417],
	[49.37815, 6.607474],
	[49.377895, 6.604801],
	[49.377117, 6.602314],
	[49.376078, 6.599949],
	[49.375864, 6.598452],
	[49.375421, 6.596432],
	[49.375264, 6.596027],
	[49.375047, 6.595875],
	[49.375047, 6.595875],
	[49.374773, 6.595937],
	[49.373408, 6.597078],
	[49.370162, 6.599006],
	[49.369746, 6.599389],
	[49.369318, 6.599917],
	[49.368762, 6.600953],
	[49.367171, 6.603363],
	[49.366138, 6.605766],
	[49.366138, 6.605766],
	[49.364737, 6.607883],
	[49.364281, 6.608333],
	[49.36153, 6.609232],
	[49.359287, 6.611279],
	[49.358721, 6.611495],
	[49.358442, 6.611271],
	[49.358013, 6.610007],
	[49.357138, 6.60848],
	[49.356943, 6.607633],
	[49.356847, 6.607498],
	[49.356654, 6.607518],
	[49.356559, 6.607857],
	[49.356559, 6.607857],
	[49.357303, 6.610178],
	[49.357328, 6.611201],
	[49.357709, 6.612775],
	[49.357724, 6.615671],
	[49.357597, 6.615845],
	[49.35524, 6.615936],
	[49.355059, 6.614754],
	[49.3545, 6.614264],
	[49.35434, 6.613008],
	[49.354157, 6.612617],
	[49.353861, 6.612514],
	[49.352411, 6.61295],
	[49.351966, 6.612865],
	[49.351966, 6.612865],
	[49.351365, 6.61227],
	[49.349548, 6.609942],
	[49.348936, 6.609635],
	[49.348072, 6.609871],
	[49.34759, 6.610173],
	[49.346583, 6.611466],
	[49.346237, 6.612196],
	[49.345745, 6.61493],
	[49.345446, 6.615593],
	[49.344604, 6.614138],
	[49.3437, 6.611927],
	[49.3437, 6.611927],
	[49.343379, 6.609695],
	[49.342565, 6.607241],
	[49.340609, 6.602122],
	[49.339869, 6.599098],
	[49.339684, 6.599342],
	[49.339647, 6.601308],
	[49.339348, 6.602374],
	[49.337955, 6.60371],
	[49.337955, 6.60371],
	[49.336391, 6.605667],
	[49.335664, 6.606248],
	[49.334212, 6.607089],
	[49.330749, 6.606674],
	[49.329401, 6.605893],
	[49.327264, 6.605233],
	[49.325846, 6.605411],
	[49.325846, 6.605411],
	[49.324292, 6.605262],
	[49.319328, 6.606664],
	[49.3184, 6.60731],
	[49.317811, 6.608057],
	[49.317472, 6.608703],
	[49.316534, 6.611473],
	[49.316072, 6.613858],
	[49.3151, 6.615798],
	[49.314827, 6.616144],
	[49.3143, 6.61633],
	[49.3143, 6.61633],
	[49.3131, 6.615912],
	[49.310819, 6.615841],
	[49.310218, 6.615478],
	[49.30948, 6.614712],
	[49.308783, 6.614446],
	[49.308418, 6.615433],
	[49.307161, 6.615594],
	[49.306472, 6.615997],
	[49.305571, 6.617214],
	[49.304259, 6.618578],
	[49.303876, 6.619216],
	[49.303876, 6.619216],
	[49.303531, 6.620384],
	[49.303314, 6.624758],
	[49.302937, 6.626186],
	[49.30229, 6.627328],
	[49.30004, 6.629968],
	[49.299227, 6.631082],
	[49.297748, 6.633628],
	[49.297367, 6.634664],
	[49.297369, 6.634501],
	[49.297369, 6.634501],
	[49.297019, 6.650689],
	[49.298326, 6.648777],
	[49.299576, 6.647309],
	[49.30048, 6.645821],
	[49.300865, 6.645379],
	[49.301661, 6.645108],
	[49.302833, 6.64548],
	[49.303192, 6.64534],
	[49.303984, 6.644702],
	[49.305146, 6.644645],
	[49.305146, 6.644645],
	[49.305933, 6.644894],
	[49.3097, 6.647637],
	[49.311187, 6.648409],
	[49.313154, 6.649161],
	[49.31628, 6.651441],
	[49.317023, 6.65254],
	[49.317023, 6.65254],
	[49.317356, 6.652836],
	[49.319173, 6.6535],
	[49.319743, 6.653542],
	[49.320212, 6.653296],
	[49.324127, 6.648491],
	[49.324823, 6.648143],
	[49.325435, 6.648328],
	[49.326984, 6.649963],
	[49.326984, 6.649963],
	[49.327756, 6.650488],
	[49.333058, 6.652732],
	[49.333273, 6.652934],
	[49.333451, 6.653478],
	[49.333389, 6.657199],
	[49.333153, 6.660121],
	[49.333317, 6.663742],
	[49.333133, 6.664225],
	[49.333133, 6.664225],
	[49.332475, 6.664988],
	[49.331919, 6.666597],
	[49.33123, 6.668011],
	[49.330937, 6.669351],
	[49.330658, 6.674745],
	[49.33067, 6.676107],
	[49.331327, 6.681018],
	[49.331327, 6.681018],
	[49.331478, 6.683832],
	[49.331232, 6.686955],
	[49.330887, 6.687475],
	[49.330734, 6.688224],
	[49.33036, 6.68923],
	[49.329921, 6.689683],
	[49.329781, 6.69006],
	[49.329743, 6.691901],
	[49.32984, 6.692202],
	[49.329999, 6.692098],
	[49.331385, 6.688654],
	[49.331481, 6.688653],
	[49.331504, 6.688835],
	[49.330501, 6.692873],
	[49.330501, 6.692873],
	[49.329822, 6.69405],
	[49.329729, 6.694821],
	[49.330116, 6.696232],
	[49.33024, 6.697961],
	[49.330176, 6.702174],
	[49.330483, 6.707415],
	[49.330829, 6.71016],
	[49.330829, 6.71016],
	[49.33151, 6.713769],
	[49.331447, 6.714805],
	[49.331265, 6.715518],
	[49.332181, 6.715545],
	[49.333456, 6.716005],
	[49.333345, 6.716095],
	[49.333456, 6.716005],
	[49.335951, 6.716914],
	[49.336546, 6.716976],
	[49.337044, 6.716871],
	[49.337648, 6.716464],
	[49.338162, 6.7159],
	[49.3386, 6.715194],
	[49.339075, 6.714116],
	[49.339075, 6.714116],
	[49.339825, 6.711705],
	[49.341643, 6.707346],
	[49.343438, 6.703919],
	[49.344253, 6.701923],
	[49.345234, 6.700469],
	[49.346307, 6.699494],
	[49.346647, 6.69938],
	[49.347835, 6.699791],
	[49.347835, 6.699791],
	[49.348876, 6.700712],
	[49.349826, 6.70104],
	[49.350615, 6.701056],
	[49.351782, 6.700838],
	[49.352884, 6.700368],
	[49.353545, 6.699924],
	[49.354306, 6.699008],
	[49.357378, 6.69293],
	[49.357378, 6.69293],
	[49.358097, 6.691778],
	[49.36014, 6.689327],
	[49.3625, 6.687717],
	[49.363269, 6.68735],
	[49.363963, 6.687432],
	[49.364193, 6.687096],
	[49.365335, 6.686803],
	[49.365452, 6.686879],
	[49.365535, 6.686732],
	[49.366722, 6.686752],
	[49.369336, 6.687285],
	[49.369336, 6.687285],
	[49.370277, 6.687158],
	[49.370922, 6.686576],
	[49.372741, 6.683634],
	[49.373563, 6.682519],
	[49.37614, 6.680066],
	[49.376499, 6.680766],
	[49.377866, 6.682805],
	[49.378827, 6.684002],
	[49.378827, 6.684002],
	[49.380878, 6.686167],
	[49.381603, 6.687163],
	[49.382805, 6.688225],
	[49.38455, 6.689233],
	[49.385244, 6.689437],
	[49.387365, 6.680558],
	[49.387365, 6.680558],
	[49.389639, 6.675482],
	[49.389951, 6.675814],
	[49.390682, 6.675577],
	[49.391377, 6.674949],
	[49.391823, 6.675243],
	[49.391981, 6.675202],
	[49.392375, 6.674002],
	[49.392634, 6.673552],
	[49.393237, 6.673455],
	[49.393849, 6.673611],
	[49.394884, 6.672176],
	[49.39617, 6.671481],
	[49.397567, 6.669992],
	[49.397567, 6.669992],
	[49.401278, 6.667814],
	[49.403172, 6.665617],
	[49.404602, 6.664204],
	[49.405005, 6.664038],
	[49.405569, 6.664173],
	[49.406036, 6.664661],
	[49.406184, 6.66499],
	[49.406408, 6.665818],
	[49.406728, 6.668101],
	[49.407054, 6.668867],
	[49.40724, 6.670143],
	[49.408602, 6.669911],
	[49.408602, 6.669911],
	[49.409408, 6.670893],
	[49.410104, 6.671267],
	[49.410624, 6.671262],
	[49.411322, 6.670878],
	[49.41183, 6.670135],
	[49.412187, 6.668794],
	[49.412581, 6.66445],
	[49.412606, 6.662436],
	[49.413197, 6.659197],
	[49.41401, 6.657846],
	[49.41401, 6.657846],
	[49.414494, 6.657288],
	[49.417089, 6.656581],
	[49.418667, 6.654822],
	[49.419316, 6.6536],
	[49.419515, 6.652797],
	[49.419816, 6.652148],
	[49.419832, 6.651288],
	[49.420004, 6.650526],
	[49.419975, 6.650126],
	[49.41962, 6.649217],
	[49.419268, 6.647835],
	[49.418771, 6.646782],
	[49.418497, 6.645821],
	[49.418502, 6.644852],
	[49.418502, 6.644852],
	[49.418758, 6.644007],
	[49.419716, 6.642275],
	[49.421031, 6.640814],
	[49.422681, 6.63971],
	[49.425438, 6.637188],
	[49.426661, 6.636245],
	[49.427494, 6.635006],
	[49.427598, 6.634439],
	[49.427598, 6.634439],
	[49.435818, 6.6346],
	[49.437211, 6.635095],
	[49.437843, 6.634659],
	[49.438577, 6.634658],
	[49.439225, 6.634787],
	[49.440031, 6.635418],
	[49.440344, 6.635467],
	[49.44049, 6.63579],
	[49.441255, 6.635996],
	[49.442037, 6.635928],
	[49.44199, 6.636346],
	[49.442102, 6.637118],
	[49.442465, 6.636973],
	[49.442465, 6.636973],
];

""" + flaechen + """

var line = L.polyline(latlngs, {color: 'red', smoothFactor: 2})

""" + fn + """

var uni_trier = L.marker({lon: 6.6866,lat: 49.7474}, {icon: digital_viez}).bindPopup('<p><b>Universit&auml;t Trier</b></br>Standort des Digital Viez Projekts<br><a href="mailto:digital-viez@uni-trier.de"><img src= "assets/bootstrap-icons/envelope-fill.svg" alt = "E-Mail" height = "12px" width = "auto"> E-Mail</a></p>'); 


""" + li + """
   
""" + gl + """

""" + vm + """

""" + kl + """

""" + sw + """

""" + vs + """

""" + vk + """

""" + ev + """
 
    
var viezstrasse = L.layerGroup([line]);
    
var organisationen = L.layerGroup([uni_trier]);

var standard = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {id: 'MapID', attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'});

var opnv = L.tileLayer('http://{s}.tile.memomaps.de/tilegen/{z}/{x}/{y}.png', {id: 'MapID2', attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'});

var map = L.map('map', { 
    layers: [standard, organisationen, viezstrasse]
}).setView({lon: 6.63935, lat: 49.75565}, 10);

var standardMaps = {
    "Standard": standard,
    "&Ouml;PNV": opnv,
};

var overlayMaps = {
    "<div class = 'legend'><img class = 'legend' src = 'assets/legende-icon/projekt-icon-leg.png'><p>DigitalViez</p></div>" : organisationen,
    "<div><img class = 'legend' src = 'assets/legende-icon/vereine-icon-leg.png'><p>Vereine</p></div>" : vereine,
    "<div><img class = 'legend' src = 'assets/legende-icon/gastro-icon-leg.png'><p>Gastronomien</p></div>" : gastro,
	"<div><img class = 'legend' src = 'assets/legende-icon/hersteller-icon-leg.png'><p>Keltereien</p></div>" : keltereien,
    "<div><img class = 'legend' src = 'assets/legende-icon/automaten-icon-leg.png'><p>Automaten</p></div>" : vending_machine,
    "<div><img class = 'legend' src = 'assets/legende-icon/attraktionen-icon-leg.png'><p>Sehensw&uuml;rdigkeiten</p></div>": sehenswuerdigkeiten,
    "<div><img class = 'legend' src = 'assets/legende-icon/viezstrasse-icon-leg.png'><p>Viezstra&szlig;e</p></div>" : viezstrasse,
    "<div><img class = 'legend' src = 'assets/legende-icon/viezstrasse-icon-leg.png'><p>Mitglieder der Viezstra&szlig;e</p></div>" : mitglieder_viezstrasse,
    "<div><img class = 'legend' src = 'assets/legende-icon/verkauf-icon-leg.png'><p>Verkaufsstellen</p></div>":verkaufsstellen
};

L.control.layers(standardMaps, overlayMaps).addTo(map);
// show the scale bar on the lower left corner
L.control.scale({imperial: true, metric: true}).addTo(map);

var oms = new OverlappingMarkerSpiderfier(map);

""" + markers + """

for (var i = 0; i < markers.length; i ++){
oms.addMarker(markers[i]);
}

</script>
  </body>
</html>
    """
    return string

# Datei wird beschrieben
htmlfile = open("viezkarte.html", "w")
htmlfile.write(printhtml(makelist(getdata())))
htmlfile.close()
