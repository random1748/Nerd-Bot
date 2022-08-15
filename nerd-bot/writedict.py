import json
emojidict = {
        1: "https://g.redditmedia.com/hoPFXn9ZeK5egX_LkAxWlvYypj-myYxVXYPDPi4BiQ8.gif?fm=mp4&mp4-fragmented=false&s=af8be3adc9026b7d91de3435beed058d",
        2: "https://i.makeagif.com/media/10-28-2015/QFCG2S.gif",
        3: "https://c.tenor.com/o2FDzwgIeOYAAAAM/ok-and-planet-explode.gif",
        4: "http://i0.wp.com/media1.tenor.com/images/ad7f97ec3837ce65b5df9de218c1ecfd/tenor.gif?resize=650,400",
        5: "https://c.tenor.com/M8UQ9PZfw7cAAAAC/space-explosion.gif",
        6: "https://c.tenor.com/mbCGoZWS91oAAAAd/spacex-fail.gif",
        7: "http://i.imgur.com/mqvaPIQ.gif",
        8: "https://c.tenor.com/-3oxN3fRb3sAAAAC/hoverboard-muslim.gif",
        9: "https://i.imgur.com/g3ImYQD.gif",
        10: "https://i.kym-cdn.com/photos/images/original/000/863/254/c5c.gif"
    }

with open('bpcfile.json', "w") as outfile:
    json.dump(emojidict, outfile)

with open("bpcfile.json") as json_file:
    emojidict = json.load(json_file)
 
    # Print the type of data variable
    print(emojidict)
