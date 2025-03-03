from flask import Flask, render_template, Response
from pyboy import PyBoy
import io
import threading
import time
from utils.dectopoke import pokemon_map, regions


app = Flask(__name__)

# Initialize PyBoy (replace 'path/to/your/rom.gb' with the actual path)
pyboy = PyBoy('red/red.gb')

#Global image variable
current_frame = None
frame_lock = threading.Lock()

# memory addresses
PARTY_SIZE_ADDRESS = 0xD163
X_POS_ADDRESS, Y_POS_ADDRESS = 0xD362, 0xD361
MAP_N_ADDRESS = 0xD35E
BADGE_COUNT_ADDRESS = 0xD356

LEVELS_ADDRESSES = [0xD18C, 0xD1B8, 0xD1E4, 0xD210, 0xD23C, 0xD268]
PARTY_ADDRESSES = [0xD164, 0xD165, 0xD166, 0xD167, 0xD168, 0xD169]
OPPONENT_LEVELS_ADDRESSES = [0xD8C5, 0xD8F1, 0xD91D, 0xD949, 0xD975, 0xD9A1]

EVENT_FLAGS_START_ADDRESS = 0xD747
EVENT_FLAGS_END_ADDRESS = 0xD886
MUSEUM_TICKET_ADDRESS = 0xD754

HP_ADDRESSES = [0xD16C, 0xD198, 0xD1C4, 0xD1F0, 0xD21C, 0xD248]
MAX_HP_ADDRESSES = [0xD18D, 0xD1B9, 0xD1E5, 0xD211, 0xD23D, 0xD269]

MONEY_ADDRESS_1 = 0xD347
MONEY_ADDRESS_2 = 0xD348
MONEY_ADDRESS_3 = 0xD349

class PartyPoke():
   name = ""
   currentHp = ""
   maxHp = ""

def get_game_coords(pyboy: PyBoy):
        return (pyboy.memory[X_POS_ADDRESS], pyboy.memory[Y_POS_ADDRESS], pyboy.memory[MAP_N_ADDRESS])

def get_party(pyboy: PyBoy):
        party = []
        for i in range(len(PARTY_ADDRESSES)):
            dec_value = pyboy.memory[PARTY_ADDRESSES[i]]
            x = PartyPoke()
            x.name = pokemon_map.get(dec_value)
            x.currentHp = "" + str(pyboy.memory[HP_ADDRESSES[i]]) + "" + str(pyboy.memory[HP_ADDRESSES[i] + 1])
            x.maxHp = "" + str(pyboy.memory[MAX_HP_ADDRESSES[i]]) + "" + str(pyboy.memory[MAX_HP_ADDRESSES[i] + 1])
            party.append(x)
        return party


def run_pyboy():
    global current_frame
    pyboy.game_wrapper.start_game()
    with open("state_file.state", "rb") as f:
      pyboy.load_state(f)
    while True:
        pyboy.tick()
        with frame_lock:
            current_frame = pyboy.screen.image.resize((640, 640))
        time.sleep(0.01)

def run_flask():
    app.run(debug=False, threaded=True, host="0.0.0.0", port="8000", use_reloader=False)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/a')
def press_a():
  pyboy.button('a', delay=15)
  return Response("a pressed", mimetype='text/plain')

@app.route('/b')
def press_b():
  pyboy.button('b', delay=15)
  return Response("b pressed", mimetype='text/plain')

@app.route('/down')
def press_down():
  pyboy.button('down', delay=15)
  return Response("down pressed", mimetype='text/plain')


@app.route('/up')
def press_up():
  pyboy.button('up', delay=15)
  return Response("up pressed", mimetype='text/plain')


@app.route('/left')
def press_left():
  pyboy.button('left', delay=15)
  return Response("left pressed", mimetype='text/plain')



@app.route('/right')
def press_right():
  pyboy.button('right', delay=15)
  return Response("right pressed", mimetype='text/plain')



@app.route('/start')
def press_start():
  pyboy.button('start', delay=15)
  return Response("start pressed", mimetype='text/plain')



@app.route('/select')
def press_select():
  pyboy.button('select', delay=15)
  return Response("select pressed", mimetype='text/plain')

def generate_frames():
    global current_frame
    while True:
        with frame_lock:
          if current_frame is None:
            continue
          img_io = io.BytesIO()
          current_frame.save(img_io, 'PNG')
          img_io.seek(0)
          frame_data = img_io.read()
        yield (b'--frame\r\n'
                b'Content-Type: image/png\r\n\r\n' + frame_data + b'\r\n')
        time.sleep(0.05)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/frame')
def frame():
    global current_frame
    with frame_lock:
      if current_frame is None:
        return Response(status=503)  # Return error if screen is not available
      img_io = io.BytesIO()
      current_frame.save(img_io, 'PNG')
      img_io.seek(0)
      return Response(img_io.read(), mimetype='image/png')
    
@app.route('/save')
def saveGame():
    with open("state_file.state", "wb") as f:
      f.seek(0)
      pyboy.save_state(f)
    return Response("Game Saved", mimetype='text/plain')

def getAvailableMoves():
   collisionArea = pyboy.game_wrapper.game_area_collision()
   m = {}
   m["left"] = collisionArea[8][7] == 1
   m["right"] = collisionArea[8][10] == 1
   m["up"] = collisionArea[7][8] == 1
   m["down"] = collisionArea[10][8] == 1
   return m

@app.route('/state')
def state():
    x,y,map = get_game_coords(pyboy=pyboy)
    regionName = ""
    for region in regions:
       if region["id"] == str(map):
          regionName = region["name"]
    party = get_party(pyboy=pyboy)
    partyAsText = ""
    moves = getAvailableMoves()
    movesTxt = ""
    for k in moves:
       if moves[k]:
          movesTxt = movesTxt + k + ","
    for i in range(len(party)):
        partyAsText += "Pokemon " + str(i+1) + ": " + party[i].name + " HP: " + str(party[i].currentHp) + "/" + str(party[i].maxHp) + "\n"
    return Response(
       "GameCoords: X: " 
       + str(x) 
       + ", Y: " 
       + str(y)
       +"\nArea Name:"
       + str(regionName)
       + "\nParty: " 
       + partyAsText
       + "\nAvailable Key Presses: " + movesTxt,
       mimetype='text/plain')

@app.route('/collision')
def collision():
   return Response(str(pyboy.game_wrapper.game_area_collision()), mimetype="text/plain")

if __name__ == '__main__':
    run_pyboy()
