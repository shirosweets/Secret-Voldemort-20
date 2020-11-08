#test for user db functions
import db_entities_relations as dbe
import db_functions as dbf
import models as md
from pony.orm import db_session

"""
@db_session
def create_lobby(
                 lobbyIn_name: str,
                 lobbyIn_creator: int, #str,
                 lobbyIn_max_players: int, 
                 lobbyIn_min_players: int):
    lobby1= dbe.Lobby(
                    lobby_name = lobbyIn_name, 
                    lobby_creator = dbe.User[lobbyIn_creator].user_name, #lobbyIn_creator,
                    lobby_max_players = lobbyIn_max_players, 
                    lobby_min_players = lobbyIn_min_players)
    return lobby1
"""
# Creando el User[0]
"""
# user entity
class User(db.Entity):
    user_id                      = PrimaryKey(int, auto=True)              # auto is auto-incremented
    user_email                   = Required(str, unique=True)              # email can't change
    user_name                    = Required(str, unique=True, max_len=16)  # user_name can't change
    user_password                = Required(str, max_len=32)
    user_photo                   = Required(str)                           # photo is selected for default string
    user_creation_dt             = Required(datetime)
    user_lobby                   = Set('Lobby')                            # many to many relation with User-Lobby, we use '' because Player is declarated after this call
    user_player                  = Set('Player')                           # one to many relation with User-Player, we use '' because Player is declarated after this call
    user_log                     = Optional('Log')                         # one to one relation with User-Log, we use '' because Log is declarated after this call
    # For next sprint                     
    user_default_icon_id         = Optional(int)         
"""
"""
@db_session
def insert_user(email: str, username: str, password: str,
                photo: Optional[str]):
    if photo is None:
        dbe.User(
            user_email=email,
            user_name=username,
            user_password=password,
            user_photo="https://www.kindpng.com/imgv/hJhxTix_harrypotter-dobby-sticker-harry-potter-harry-potter-dobby/",
            user_creation_dt=datetime.now())
    else:
        dbe.User(
            user_email=email,
            user_name=username,
            user_password=password,
            user_photo=photo, 
            user_creation_dt=datetime.now())
"""

# User0= dbf.insert_user(
#     email= "valevispo@gmail.com",
#     username= "Valentina",
#     password= "passwordOP8",
#     photo= "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxISEhUSExIVFRUXFxUVFRUVFRUVFRUVFRUWFhUVFRUYHSggGBolGxUVITEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGhAQGi0lHSUtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0rLS0tLf/AABEIAMIBAwMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAADAAIEBQYBBwj/xAA/EAABAwIEAwUGBAUEAQUBAAABAAIRAyEEBRIxQVFhBiJxgZETMkKhscEUUtHwByNikuEVcoKi0jNjssLxJP/EABgBAAMBAQAAAAAAAAAAAAAAAAABAgME/8QAJREAAgICAgEEAwEBAAAAAAAAAAECEQMhEjFBBBMiURQyYXEF/9oADAMBAAIRAxEAPwD0hKEgurlOw4upJIASS4So2JxrWC5SCiXKFVxLW7kLIZv2rDbNKymPz2q8+9CXIrieiY3tHSZ8QVDju27W7XWAxVUm5dKhvq2S2w0jdt/iBe4KtcL26pHdeUEE8EfC0SVT0Ls9kodqqDviCtMNmFN+zgvDzRI2UnBZtVpGzj4JWDie4ykvOMv7aObAeFq8t7R0qo94J2LjRdriZTrA7FPTENcolcXUsqNXSYztBHQKKMhCEmOKcUN5TAaSmOK6Sh1CkMBUKYmvcm6lJQRcQ9a4XosKCFNlML1wvRYUElJB1rqLA0y6uLkqiTqBiMSGiSVzFYprBJK887V9oC4lrCk2NIts97WBktYZKyeKzqo/c2VE6sSbm6VSqYU7LVBMbV4gqJ+IJUZ9YhMNTiqUSXIkuc7dEpUy5ABcRsp2DtuEPQLbO0qcLrbGQiVeiC2VJVB3V4QDT1GU8U53XSQ1CEx9Nsbrntiw90kJlerKAXppA2aLKu1NakRJkL0DJu0VOuBcTyXktJ3REZUcw6mGCmSe36kCuVj+zXavVDKljzWpfVBEgoYUGolGlQ6LkfUmhMIShuKRcmkpgcKFVREOqkBBqFMJTqiYoLEuFJclIYlxJJAHEkkkAalCxFcNEkrteoGiSvP+1faIyWMKohIZ2qzwuJY0rHuknmg4is4mSVKoOGmSkUQq1CCjspSLrmLqgqEcSdlS2J6D1sKE6hhhyQKLi4qwL9IhDdCSsIWtA2QKlUcEF9U8UIbpdjeiWwmbpVaoQK9e1lEc8ooLJVWuQm6iUDXzKNh2Oe4NHEwE6oV2dqVg3e6YMaOS0GHo0mDQ5jXxc6iYPpwRxluBqO03w7uB1F9Inrqu31UqcS3CRmvbO4BEbqKtswyqpQfoqNgfC8Xa4c2n7boYwzTxV2iKZFbiC0jmtDl3aSo0AEEhVopt4CSuOov4oqw6NTR7UwbthTqXaulFzfksBWpuPHZAYSCmoicj1Gj2gpETqjxU3D45jhYg+a8ixFbjPgnYLNKjILXEJ8Rcj2UOTKqyeT9qAQGvseavsRmDA3VP3UyddlJX0cqlCLlXVsc50lrbT8QPyC5g8Tqdpi8GCDaRciPBYe4rNvbdWWMpSmgpSrIOpSmylKQHUk1dTGM7X542mwtBuvNX1tZLjumZzmDqtUkm0oRdZUyUEaJMJ1c6Qg4d11zH1bIAj1XE7IehMp1U01rp0KydQZCIx87qOH2XGPIU1ZV0SKp4JwqhougNfzUPEYiSrohskVqgcbJlV0KIxxXHy4qkiWw7TOyt8qcQZMWaf0+6gYJkKyo1B3wN9Py1BTIqPYVtQ6gbc77K7oYE1G2Dr2J1WPlKzmIqRECeF7fVXuWZlsxhDibHTufAyNlnxNm6C4TGtpTQrB76PxNMTSdsHsky0i4gTKdjMCKOlwcH03XpvGzhx8COSnuoF3eLNp1RsQeZcL7DY+aq8DimMc7D1Q8UnkFohzvZPPxgyYabyJOydUSyJiKrWmQh/jpm6tMxyEfC7vSLbggiQQeRt6qmZhHMfDhbbZaJJozk2gNaoNy7yUf23+E/E4SX3s3giYShpJkSFZmDb3t1x9CNlPptY0aqhA/pG/mU6hiKb3ENbDGiXvJs0dOp4BJuhpWLK6OrvvsxhA6udwY3r14LS4JhqkONmj3WTAHDfiVV5bhxWeHEAUm+42fKTNiSbrcYKgWidFo3EFYS+TOiK4op84LqbbNBb0t8+ap8krzXE23+hV9ntUFpiQdiCC0+kQVRZZS01xJvBPyKza2bxfxZowV3Ugh66XrQ5gsrkoOtc1ooLDykg611FBZ5IK0uPipbzZV1Ed5S67rK2SjntYUarWJTQ7qmVExWFpN5rr6aC2ohOrGd0U2KyXSsd1LAHBV9ETdWWH0hFAmAxihMEo+LqyVHaEIGF1cETD0CSo2jipXttLVRJIrVw0RxTMDULnG+7SPv9lV+0LyrCgHNu33pGmOJkWhDQ09kvEVIF1JyGpfT3RO/vGR1YwS7wULMXMa0Mc8OcbkiwE/CpvZ/E6eFhwk3+nzUxVI0k7N+0F1OHd4xZhEACLGBcSeLvILF5waodDjbcbnawuCJv4q3rZrXI7hpsaJiZcX9C51/EfZZrMqjqryX1dQiXMFgI2c0DhvI4T6BLNBkWbuewNLgagnRq2c2PcPWYjkoNLODVq6XN0wSHnxO3iqejUBA0j3eOxuN/X6rvtdNxO4jrJG6aVCcvsuXEucQGyYLmgHcNBJHoE3CYhlVzGuOlptI5i67lzzSNJ7rmXf/ABIMnzKrK2Ec5mtgIgzA4ixt5FWST80wB9p7KmwuJNjwjeTHCEyvS9k1tBogaiXOO9Qjcz+4R8uzQxfeAHcCA0+7PVTXOpvAJ965F+LhfwsVjJvyaxiu0W2RtDY1CxAg8PqR9FocRh3gFzXx0lwHgWzHyWPwrazRLNRaOg++wWswGMJp/wAxpaQNxZvqZgeIAU2jTZRY6q9pmoZPw2soeW03OrPeTPdg9CTt8ipmIFJtQEyDO0gg3uRHDy4pYvDOFUOa6KT2lzQPzjTIPUAj1Wbas3f6g8ViXMKazMyjnB62yb/b9VXHBwYV8kc/Enf6iujMVB/ClcdhilzQcGT/APUwkqw4VySOaDgzDNEORq7rJlanBQy9amXQJpHFKqE17Logp2VCI2qEIyTZGrtSwrYVkBqQIEIz6kBcda6jvrTZSUjhqSnUQU1lNSKVON0xWG9nxlQ8XV1WTMXiiLLmBlx1HZP+i/hPwWFDRJ3UzLTNZhO2ofv7qNXrd1DhwbqaDvwU9ldA+0LRrPMb8JVhkwDGEumdxB3H5mn6qpdRdVfJEDiDP2VlhWNJDLiD8LrieY++3qn4oV7sLXY94I70WkAGRJsfX6p+BwDhUZa5AgcZG9ipDMK2BqeWuabQNR6BwFnC21o6q7yZjnPZ/MbIIhjgSI4FpBOjZTdFVYF2Stplj3WD2gxtAcSQL7Q4MHmOqi4HLxVcyPdDZIPEi0DqvQO1GHYKQc1gLokNtvFw089zCrMnY1gJG0CLCSYE25woeSi1jshYHLPagl7SG/zAAOAafe9Z+SOMl9iXgguY+Awt4Q0aj4XU/Lb06kTbgeRJv4GHLS4Zocyi2xiZtzkfvwWbyNM19tUeX4rKfY1S2q8X2J/KZubXO/olh8GSJgzYAf8AHVf98Fu+3WTipocAJ2M/TpM7pmXZI0UTM7XIjlcAnb/C05pmXFopsAXsGkOkX8LX3Wio1Q9sGWk2EdFlaOKa15aA7SSQJBked/t4K+pDUB3oiCBbzPosZaZsnaMpWwzxiHMfUEAyJjYfQrVY6i38MwjmY5wRf6BZztbg3MHtWQXEyZnUfAcBHPmjZEX1RBJaBJ08CY9E6vY+fgmYZjo3gcv8oGIgHrsVY0GHdV9fRqcBv15qIfIc9HAFwtSp2sUUpNUCdgtKSKEkDMZm2XxeFn8Q2Nl6JnuG7iwOKZBK6YM5porm1DN0cVEOpTXQIWhmPeAgOrQuVKqjPcqSJYeriJ2TqLJQKLZVrh6RCHoEFw2HXMbVDRCM54aFVYglxSQ2No0dZk7Kdh6d0OgyLKzbhmhu6TYJEGuACrfBD+U3ZUVexsZV5gHTTAUy6Kh2AIaSRcA9VZMp0wBZxdtJAmOMFV74aZ/firvLMvq1mjSAfPbok5aKUdj/AMA2rp0uIcLE30geF7olPEYSh3a1cNdMwLnxJbceKi9oMortNGi6WCq8MgctyfCNSwOb1AarmtEMa4ta0f0mJPMnmnBctCySUOj1LF5xRxDRTo4lrwCOJDhycJAMo2MxWgNMQYg+O0/JeUVMMKfsnMqAlwJ7syxzSQLnwXoNHFHEYFlbiPejm0aT9JUzxcXorHl5rfZuezbA+g8n4rHa0CP/ALH0WowNCGNtwj5z9Viewzu4BwIj/kbnfoAvQqLJAA34ev6lYSWzW/iVOeYZ72lo3F+U7KtxGKpMpex9rTBiDL2l0/7Z5qP/ABYzNzGewY8sApOr13MMPLAdNOm13w6nB0nk3qvAsFh3YirA3JncCATG7tzfitceC29mU89JKj23EZGQdbWgzxADtzfiZR8CdFtJ1TeRtP75Lz3KcW7CVHtpVy5lKq2m7cMe12zg3YHceUr0bU/UCWOdxgB3HndRlXF0zXE+StFo7K/aM0m83AsQPkELLcr9nMAHfgAPICymYPE93SWlnTj8kVlUb/ZKIMzDqpZqgAXO9oVBUxDjVJN+SNmmJd+IfTjifJQtYa43k9VeONEzlfRZ+21O4KQ1qrKD9RnjyVtTnioyKmXB2hns0kWV1ZlgM/aBTK8rzKpDit323xLmiAV55jri668aOXK/B2i8FGq4eyhZfur7RIVy0Zx2ZyoyE6jSngrCvhrouFpgJ8tBRCw9AyrmjYbBdp4YFGqUg0KWykiqxlRQ6RujYsXKZhN1RD7JuBpmdR2R8RVmwSYeEpjmmVJYD2A3+amMe7SAAOvNce30G5Kfg33nhKmXQ49j20g6L+asMszZ+HMNPEWM95ODGiZiOZ/woFYAOBN2eAMKEzRo9BfmFPH0RTe72FemWPovdBb7RpkSRwOx6FeWdruz9ejWc91F1MOJcZuwEm+ip7rmm5F5jcBaLB4jSRof3Z6A+sytnlnaWqQKYioNnNLZgc9RMFXGfFkTx8keGNkdTs0C8T4LddicT/8Ax1KR/ObeMenFavtHhKWIpGKdOneXQ0XIP9NvmstgqLaZgdCdoJ5nmNlcpqSIjjcHZtsgoOGktsA4HyF+C9Gy2pYTuOG/kFh8lNm6Y0wIjnx+i02Ed58eq5upWdUlcaPOu3+PbUzHEUajtNOrh24f2h92nUbL2Fx4Nl5BPULyfEYSrh6ha9hDmnkYPUEbgr6JpZLSOJfXexr9Rkhwm5EEwekLucZDgmHWzBUdczLmDSD1hbRyqJzyxNs8k7Adm6uJeC4FlD2jalWobAindrGk7md+S90fiWCwG3HkFmKTq73taQ0NGzWHSwcQdOxV9Qwu2omN4dYSspzcmawgoobmFEFuoSOQFvOyrKWMmAQR1t6K+xdDUA0mx4CfsqbEYLQ+HE9JiyKHaMjnFZjKryW7kQSVDoMfUd/KYD14DzVjUyM16znud3A7YHfxKviG0GwwNEbDZXySIpszjcFUY6XtPUjbyUwAnmtBQxLarYIvxtsoNTCwok7LjordCSlFiSxNDK9tKJJmLLz3NiAvUO2lTuaYXmWPwJN1145pdnNli/BBwdS602EfIWdo4OCrrCEgLSckzOMWguIag0nIj5USu8hIbLSjUCNiIiyosPijKttUtSaGmVWMF0DDk7KdXHRRg9rdxdUuiX2SaZiU7C95A1giVLwdgkxofjH90NG6dhqMWOxC6KEu1J9cwOUdQFLWhrsVTXGkiev0KVDCPEd8DjG4RsGdd2iecaiB4kCArWnl9MxNZjeg78/2mR6LJ2jZUytptIcCb35C3yWuwGYim34gDaIEfuFWjAYdpnU8npGk+sFTxTw5im+tpNiWuFo6E/VSt9ltUMzGmS0lxdpNxJknoOSyGaYssILranG3HSeXyW6FJsNBrMqNJPvEHSOAbFpUvMey+GxtJrZ77QfZvB4nh4LSDM5Ijdm81aGDumALR0+60uGx0wQCJ2na68hwWKxGBqVcPWMFrmxNwQTEg8W9V652VyN1Y+3fUd7E2YwWBH5ud/usZQnzpHZGeL2+TNHSw4jfe/PxUj8KD3XXHIp+Johje6Q3YCdgELDkTepxO0HyVtU6OK7VkfEZWGnUGiOWxQqlJwu1nhJ28BxV7oBG9lGrNjj903AUcn2Us1eO/h90PHVi1jnuE6RxA381Y1q491pvzWdzutrmiCY+J5gifOyUUW3fgyGJz5ru7BZ1DgPkFBbXe51nEixEkkFWWNymg24c1xkCZAM/T5IZw9IkNFRjj4OBH/LZXonZZ5diCCJBB4q0xtQc1S4UcJ2I3381ZYxs+ilrRSIpckh6ElgbA+0+C1tlYHGYaLL1LMGS0rz7NWQ4pt0KrRQfh1Lo0ITmhSmEQnyJUURHhRK9EFWbnDkhFoT5sTiiqpUADsrGkJTvYhGpUYVLIyfbI9elawVHXF1pqgsq3EUAeC1jlRnLGysHipVB4ATX4I7gwOf73QHNe33P7j73l+X93V8kyKaLZhj3jA9XHwb+sKa6lLe6wE83DV/1931BWZo4hwMaS9xNgJN/K5PgtflbgaU1XARbS2DMWIkWJ8J5EtTaaBOyFSwtRxu9z3cGCXho8BDQPOym0aTaXeqlrf6XvJnw07jq1tQLtDMDDm02imLbXceRJ4H1I5lQm4TUS6pYE+8bl7uIA3e7zjaTe+bf2aJa0ajLM4Y+1Jh3gENawuI5WcXEcwGx0UjHNe8XFN8izTL3H/lPzJI9LZR9SrTMMAFvdtYNvNd+xj8tmjlNlaYTN9IAe6XES5xkW5xu1tvG3OzZcfotSrTLfLsvEGaUGQ4Q9pYS3lbafpxWiwEsiNIETa0cxCyVHNmmCxwMxAPG/vRw2tyU3DvfUdLqjmj8rbDrssm3ezZJM5/ELE4V76BraTUY9tmyTokEtd0nmvS8izNr6bSwjSWgtusSMgovEkXO/wCkqzwmUez/APTeW+Bt6K1kIlji0azEua74Zm1jsn4SnHutAHqq7B0495080XGZ5SotMuAI+mypU3bMmmlSLXE4lrBJKz+YZkw7uZp5mw/usB6rH9qu3NNkt1GY1DRfu8+Th/8Aq8uzfP8AEVNqpa10xB1Uqg4ggje92kTta6tQlP8Awi4w77PTe0HbynS/ks9qyTpFYN9pS8jqEjqJ8CoDPa1Gfyoqzu+k4MeSeYgD/qvJKOJc0k03Gm87tB7j/AHfwM9OSusr7Tua0tJ9m4wC9gsRydT2H/GPArSWOlozjlt7PScHlTXMjUHlp/mP90yPhaBYgHd19oQ6bqYqFtOahb7w4iQSL7AqvyjtK2o0MMl7rNLT3T119N9LvktfSeym0NMQIOoADU7kf6iVhPT2dMFa0Z7A5gG4pzHfFplnFvdEHpN1dV3AuLBwGryUJ9GkxxfpEkkknfmb8VGwdR73urHusMtbbvFotJ6TPqoclRagyXqSXNSS5uR08Sbj6vdKwWY1AXFbLNqDQ0xI8ysNiqTpMFW6MqdARCM1RTSdynwKXeHApCDvATGsTG1OseNkVruqLY6H+zTxTsmKQzaydhREeCo7h5qfUYgeyPI+iFITiQ3Sd111H83dHLdx8v1hTBh3cAZ8E9uFLeI1fIfqU+aJ4MgPa1oI0xI93iR/7rtyP6RAPHrFw9UtfqcSQbHoOAAGwHIKzfgncwiUMu+JwsOXE8h+vD0WkcpDxg6dRjHNcTLXHS1o3eenIDifurOs3U1ztQBA9/ZrBwFOPqL8uZq8ZQYT7tyNPEAN/IBwb534pv8ApTXjvFxaB7uogeAAsPLqq9yDFwkTDmFJtIS4GQCNpeRs53K+w28eOVxWZOcYJ967jybuB94/28ZVo3JAZe65PDn0jlt5WVdUydxJNzO5+q1hkxLyRPHkYF+agTpmwt9vsp2E7VVWC3AHzMf4Qf8ARzyTqWSnkh5MTEseUu6H8Qq4AECIN+PRWGH/AIi1XWLeHDnt9VnqOT/0Kww+Utn3T6LGWXEukbxx5H2y4d/EGrADWk90T/uI4KqzDtHXqg92DcT0M7+gVlh8rFrD0Up+BYB7o8isfyYrpGv48n2zC+ze8aH89THcWO/8TxHgfEH4Cq0mAIMa2G7Hcj4ciNuC278A3lCQwY2sVS9c0S/RJ9mGfkr3XZ/aTceB+IfP6ppyaqeHityMCOnof0RBhJ39eP8AlS/+hIqPoYGNy7CV6LtTBB+R8RxWrpZxi3Ma06YBBIJ3jYTxHTccCpWHwQnjHgrYYFobAHEHZYz9bKT6RvH08Y6K/E4uu5l2iCBxJjptt1RctqVT77hp+EDh02U9+GG0dNk3DYEg9FDzt6NFjigxqHgx3/T/AMklK9gUlPImjmcNGmSFi8Sbm62WbVCARE25/osnWZJ2XQ2YJaK6oVxtRTPYjlHmmfhwp5IKI5dzHyTC1p4KX7D97LhodEcg4kcUuX1j6IzGu/MR6H7JzaH7upWHhsy0O8S63hBHzT5gokUsqfmB8v8AKGyo8e80+X6qaQeSQF0uf8HwA/jm6Y0EcyQ+frCG3EN5t9QrAsI3jkmmm127QfEIck/AcX9gadQbk26QfRSW1ZHCEI5ezhLfAkfRIYI8HnzR8R7HNLZ29E8NaUEYV/5mn5Jj6FQfDPgQocPplX/CWGNAj5qO7DeHmP0QHuePhd6SmDFvG7fWyaxy8Cc4kxmFPJSqOGbHXw+6rvxj4mwHMn7qRQrPMd/+0Sh45eRqcfBZ08KN1Lo4UW2UajA3cfkFNogdSsmqNESaNBvRMqYOdmk+AUmhTIv+imUz1+qLQFC/K3co8VHdlfMx8lr4tsotcKZIFOzPjKOvzunuwbRz9SrXQh1GKEmVZAomNnHzA/RHbWdzafIj9U0thJoQxujofe4+aO145H9+CABdHY1OKE2gocP2CkuQuq6IIOd7Km0jlwSSW8jOPRDqBcISSUMYmrjwkkkDONRAkkhAhzUY7LqSpABciAWXUkAjoTiEkkPoDgaOSlYZo5JJJMZMa0Tsm4ym0i4B8gkkoKM5iaYDrAegTHvIiCUkl2R3E55aZaYJoLSSJPNT8I4zuuJLin+50R/UuKeyk0Ekkg8EwbKJiFxJU+iY9g2rjkklBZCq7poSSSYzrVIppJJxJYVJJJWQf//Z"
# )

#dbf.insert_user(
#    email= "valevispo@gmail.com",
#    username= "Valentina",
#    password= "passwordOP8", 
#    photo=None 
#)

#dbf.insert_user(
#    email= "laozoka@gmail.com",
#    username= "laozoka",
#    password= "otrapasswordmuymala",
#    photo=None
#)
#dbf.insert_user(
#    email= "asesinodeabuelas@gmail.com",
#    username= "ElMatador",
#    password= "pas22swordOP8",
#    photo=None
#)
#dbf.insert_user(
#    email= "salchicacosmica@gmail.com",
#    username= "Salchicha",
#    password= "aseeswordOP8",
#    photo=None
#)
#dbf.insert_user(
#    email= "otravalentian@gmail.com",
#    username= "robaronelnombre",
#    password= "passwordOP90",
#    photo=None
#)

"""dbf.

with db_session:
    dbe.User.select().show()"""

#dbf.showDatabase()
"""
{
  "logIn_email": "laozoka@gmail.com",
  "logIn_password": "otrapasswordmuymal"
}
"""
#lobby = md.LobbyIn(lobbyIn_creator=1, lobbyIn_name="El Pato")
#dbf.create_lobby(lobby)

#dbf.join_lobby(1,1)
#dbf.join_lobby(2,1)
#dbf.join_lobby(3,1)
#dbf.join_lobby(4,1)
#
#print("Number of players: ", dbf.get_number_of_players(1))
#dbf.leave_lobby(3)
#print("Number of players: ", dbf.get_number_of_players(1))
#dbf.showDatabase()
#dbf.join_lobby(3,1)
#print(dbf.is_user_in_lobby(1,1))
#print(dbf.is_user_in_lobby(2,1))
#print(dbf.is_user_in_lobby(3,1))
#print(dbf.is_user_in_lobby(4,1))
#print(dbf.is_user_in_lobby(5,1))

#print(f"The players in lobby 1 are : {dbf.get_players_lobby(1)}")
#print(f"With nicks: {[p.player_nick for p in dbf.get_players_lobby(1)]}")
dbf.showDatabase()
#print("\n get_player_id_from_lobby: ")
#print(dbf.get_player_id_from_lobby(2,1))
#print(dbf.get_player_id_from_lobby(1,1))
#print("\n No")
#print(dbf.get_player_id_from_lobby(6,1))
#print("\n Si")
#print(dbf.get_player_id_from_lobby(6,2))
#print("\n No lobby")
#print(dbf.get_player_id_from_lobby(6,3))
#print("\n User 12")
#print(dbf.get_player_id_from_lobby(12,2))
#print("\n User 12 lobby 3")
#print(dbf.get_player_id_from_lobby(12,3))

#print(f"\n Nick Player[1]: {dbf.get_player_nick_by_id(1)}")

"""
# Pasar jugadores al Game
@db_session
def join_game(current_player: int, game_id : int): # Final
    #Add current_player from a Game
    g = dbe.Game[game_id] # Game
    dbe.Player[current_player].player_game = g
"""

# Testing Join Lobby

#try_lobby= dbf.join_game(1, 2)

#####################
# in terminal
#venv activated
#python
#from db_entities_relations import *
#from db_functions import * 
# Lobby.select().show()