import geopy.distance as gp
import datetime as dt
import gmaps
import folium
import googlemaps

# API Google Maps
gmaps.configure(api_key='AIzaSyAnTdP5rBkeSKmf0Z0SYAXdPdYxXzFKZwY')
gmaps_client = googlemaps.Client(key='AIzaSyAnTdP5rBkeSKmf0Z0SYAXdPdYxXzFKZwY')

# Cadastros cidades
cidades = {
    'Cidade': ['Curitiba/PR', 'Londrina/PR', 'Foz do Iguaçu/PR', 'União da Vitória/PR', 'Joinville/SC', 'Chapecó/SC', 'Porto Alegre/RS', 'Uruguaiana/RS', 'Pelotas/RS'],
    'Endereço': ['Av. Comendador Franco 188', 'R. Martinho Lutero 200', 'Av. Por do Sol 210', 'R. Treza de Maio 772', 'R. das Violetas 900', 'R. Mato grosso 55', 'R. Nunes 15', 'R. Paineiras 30', 'R. uruguai 85'],
    'Lat': [-25.46648943139926, -23.324629724203593, -25.540716987708834, -26.231916965966228, -26.300139914264992, -27.106206468103967, -30.0701603481891, -29.78043464348366, -31.77765702348406],
    'Long': [-49.233462526403486, -51.1879843263008, -54.55070015174274, -51.08049757601783, -48.828195134249775, -52.620388979337626, -51.21018290938112, -57.07663023612113, -52.33972572147659]
}

agora = dt.datetime.now()
agora_string = agora.strftime("%A %d %B %y %I:%M")
agoradt = dt.datetime.strptime(agora_string, "%A %d %B %y %I:%M")

#//////////////////////////////////////////////origem
print("Escolha uma cidade de origem:")
for i, cidade in enumerate(cidades['Cidade']):
    print(f"{i + 1}. {cidade}")

escolha = int(input("Digite o número da cidade desejada: "))
if 1 <= escolha <= len(cidades['Cidade']):
    cidade_escolhida = cidades['Cidade'][escolha - 1]
    lat = cidades['Lat'][escolha - 1]
    long = cidades['Long'][escolha - 1]
else:
    print("Escolha inválida. Por favor, digite um número válido.")

#//////////////////////////////////////////////destino
print("Escolha uma cidade de destino:")
for i, cidade in enumerate(cidades['Cidade']):
    print(f"{i + 1}. {cidade}")
escolha1 = int(input("Digite o número da cidade desejada: "))
if 1 <= escolha1 <= len(cidades['Cidade']):
    cidade_escolhida1 = cidades['Cidade'][escolha1 - 1]
    lat1 = cidades['Lat'][escolha1 - 1]
    long1 = cidades['Long'][escolha1 - 1]
else:
    print("Escolha inválida. Por favor, digite um número válido.")

#//////////////////////////

latf = (lat, long)
longf = (lat1, long1)
dist = round(gp.distance(latf, longf).km, 2)
custo = round((dist * 20), 2)
tempo = round((dist / 100), 2)

print(f"A menor distância para o destino é de: {dist} Quilômetros")
print(f"O custo do transporte será de {custo} R$")
print(f"O tempo médio será de {tempo} horas")

if dist > 500:
    print("A distância é maior que 500 km. O caminhão vai parar e continuará no dia seguinte.")

    # data e hora de chegada considerando parada
    data_chegada_parada = agora + dt.timedelta(days=1, hours=8)

    print(f"Data e hora estimada de chegada no dia seguinte às 8 da manhã: {data_chegada_parada}")

    # direções API google Maps
    direcoes = gmaps_client.directions(
        (lat, long),
        (lat1, long1),
        mode="driving",)

    # mapa folium
    m = folium.Map(location=(lat, long), zoom_start=8)

    # marcadores origem e destino
    folium.Marker([lat, long], popup=f'Origem: {cidade_escolhida}').add_to(m)
    folium.Marker([lat1, long1], popup=f'Destino: {cidade_escolhida1}').add_to(m)

    if direcoes is not None:
        # rota origem ate destino
        coord_rota = []
        for leg in direcoes:
            for step in leg["legs"]:
                for point in step["steps"]:
                    start_loc = (point["start_location"]["lat"], point["start_location"]["lng"])
                    end_loc = (point["end_location"]["lat"], point["end_location"]["lng"])
                    coord_rota.extend([start_loc, end_loc])

        folium.PolyLine(coord_rota, color='blue', weight=2.5, opacity=1).add_to(m)

    # gerar mapa em html
    m.save('rota_mapa.html')
else:
    direcoes = gmaps_client.directions(
        (lat, long),
        (lat1, long1),
        mode="driving",)
    
    coord_rota = []
    for leg in direcoes:
        for step in leg["legs"]:
            for point in step["steps"]:
                start_loc = (point["start_location"]["lat"], point["start_location"]["lng"])
                end_loc = (point["end_location"]["lat"], point["end_location"]["lng"])
                coord_rota.extend([start_loc, end_loc])

    m = folium.Map(location=(lat, long), zoom_start=8)

    folium.Marker([lat, long], popup=f'Origem: {cidade_escolhida}').add_to(m)
    folium.Marker([lat1, long1], popup=f'Destino: {cidade_escolhida1}').add_to(m)
    folium.PolyLine(coord_rota, color='blue', weight=2.5, opacity=1).add_to(m)
    m.save('rota_mapa.html')
