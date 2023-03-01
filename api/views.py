from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection
import json
from django.db import connection




# Create your views here.

# load_dotenv()

# client_id = os.getenv("CLIENT_ID")
# client_secret = os.getenv("CLIENT_SECRET")


# def getToken():
    
#     auth_string = client_id+':'+client_secret
#     auth_bytes = auth_string.encode('utf-8')
#     auth_base64 = str(base64.b64encode(auth_bytes),'utf-8')

#     url = "https://accounts.spotify.com/api/token"

#     headers={
#         "Authorization": 'Basic '+ auth_base64,
#         "Content-Type":'application/x-www-form-urlencoded'
#     }

#     data ={
#          "grant_type": 'client_credentials'
#     }


#     result = post(url , headers=headers , data=data)

#     result_json = json.loads(result.content)
#     return result_json['access_token']

    
# @api_view(['GET'])
# def get_music(request):
#     sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
#     data = []
#     results = sp.playlist_items('0vvXsWCC9xrXsKd4FyS8kM',limit=5, market=None)
    
#     for idx, item in enumerate(results['items']):
#         itemObj = {}
#         track = item['track']
#         album = track['album']

#         itemObj['track_id'] = track['id']
#         itemObj['track_name'] = track['name']
#         itemObj['track_link'] = track['external_urls']['spotify']
#         itemObj['track_cover'] = album['images']
#         itemObj['artist_name'] = track['artists'][0]['name']
#         data.append(itemObj)

#     return Response({"data":data,"status":1,"errorMessage":""})


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


@api_view(['GET'])
def get_environment(request):
    sql = "select * from public.scenes as s full outer join public.audio as a  on s.scene_id = a.scene_id"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = dictfetchall(cursor)
        
    return Response({"data":rows , "status":1, "errorMessage":""})


@api_view(['POST'])
def get_or_create_user(request):
    data  = json.loads(request.body)

    email = data['email']
    is_active = True
    name = data['name']
    profile_pic = data['picture']
    print(data)
    with connection.cursor() as cursor:
        cursor.execute("select * from public.user where email=%s",[email])
        row = dictfetchall(cursor)
        print(len(row))
    
        if len(row)== 0:
            print('success inside')
            try:
                with connection.cursor() as cursor:
                    cursor.execute('insert into public.user(name, email , is_active , profile_pic) values(%s, %s, %s ,%s)',[name , email , is_active , profile_pic])
                    cursor.execute("select * from public.user where email=%s",[email])
                    row = dictfetchall(cursor)
                    print('success',' ',row)
                    return Response({'data':row,'status':1, 'errorMessage':''})
            except Exception as error:
                print(error)


    return Response({'data':row,'status':1, 'errorMessage':''})

@api_view(['POST'])
def logout_user(request):
    data = json.loads(request.body)
    
    email = data[0]['email']


    with connection.cursor() as cursor:
        cursor.execute('update public.user set is_active=false where email=%s',[email])
        cursor.execute('select is_active from public.user where email=%s',[email])
        row = dictfetchall(cursor)
        print(row)

    return Response({'data':"",'status':1 , 'errorMessage':''})