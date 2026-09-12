from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

FLAG1 = "CTF{th3_bl00dy_g4t3_0p3ns}"
FLAG2 = "CTF{r4v3ns_c4rry_s3cr3ts}"
FLAG3 = "CTF{th3_m00n_d00r_4wa1ts}"
FLAG4 = "CTF{4s_h1gh_4s_h0n0r}"

# ---------- Shared Arryn theme ----------
ARRYN_HEAD = """
<!DOCTYPE html>
<html>
<head>
<title>The Vale of Arryn</title>
<style>
  body {
    background: #6fa8dc;
    color: #f5f5f5;
    font-family: Georgia, serif;
    text-align: center;
    padding: 40px;
  }
  h1 { font-size: 2.5em; letter-spacing: 3px; }
  h2 { color: #ffffff; }
  .sigil { font-size: 4em; margin: 10px; }
  .box {
    background: rgba(0,0,0,0.25);
    border: 2px solid #ffffff;
    border-radius: 12px;
    padding: 20px;
    max-width: 640px;
    margin: 20px auto;
  }
  .motto { font-style: italic; color: #e8f0ff; }
  code { background: #0b3d6b; padding: 4px 8px; border-radius: 4px; }
</style>
</head>
<body>
<div class="sigil">🦅</div>
<h1>House Arryn</h1>
<p class="motto">"As High as Honor"</p>
"""

ARRYN_FOOT = "</body></html>"

# ---------- Stage 1: The Bloody Gate ----------
@app.route("/")
def home():
    page = ARRYN_HEAD + """
    <div class="box">
      <h2>Welcome to the Vale of Arryn</h2>
      <p>The Eyrie stands, and the Bloody Gate is shut.</p>
      <p>Only those who speak the words may pass.</p>
      <!-- The Bloody Gate answers only to those who speak the words:
           /bloody-gate?pass=As_High_as_Honor -->
    </div>
    """ + ARRYN_FOOT
    return page

@app.route("/bloody-gate")
def bloody_gate():
    if request.args.get("pass") == "As_High_as_Honor":
        return ARRYN_HEAD + f"""
        <div class="box">
          <h2>The Bloody Gate Opens</h2>
          <p>The Knight of the Gate nods. You may enter.</p>
          <p><strong>Flag 1:</strong> {FLAG1}</p>
          <p>Hint: carry this key to <code>/eyrie?key=...</code></p>
        </div>
        """ + ARRYN_FOOT
    return ARRYN_HEAD + """
    <div class="box">
      <h2>The Bloody Gate Remains Shut</h2>
      <p>"Who would pass the Bloody Gate?"</p>
    </div>
    """ + ARRYN_FOOT

# ---------- Stage 2: The Eyrie's Raven ----------
RAVEN_SCROLL = "V29yZCBmcm9tIHRoZSBFeXJpZTogQ1RGe3I0djNuNV9jNHJyeV9zM2NyM3RzfQ=="

@app.route("/eyrie")
def eyrie():
    if request.args.get("key") != FLAG1:
        return ARRYN_HEAD + """
        <div class="box">
          <h2>The Eyrie's Gates Are Barred</h2>
          <p>"You are not welcome in the Eyrie."</p>
        </div>
        """ + ARRYN_FOOT
    return ARRYN_HEAD + f"""
    <div class="box">
      <h2>A Raven From the Maester's Tower</h2>
      <p>The scroll is written in a tongue you do not recognize:</p>
      <p><code>{RAVEN_SCROLL}</code></p>
      <p>Hint: the raven's words must be decoded before the Moon Door
         will answer. Bring the decoded value to <code>/moon-door?key=...</code></p>
    </div>
    """ + ARRYN_FOOT

# ---------- Stage 3: The Moon Door ----------
@app.route("/moon-door")
def moon_door():
    if request.args.get("key") != FLAG2:
        return ARRYN_HEAD + """
        <div class="box">
          <h2>The Moon Door</h2>
          <p>"Only the Lord or Lady of the Eyrie may open the Moon Door."</p>
        </div>
        """ + ARRYN_FOOT

    rank = request.cookies.get("rank", "guest")

    if rank != "lord" and rank != "lady":
        resp = make_response(ARRYN_HEAD + """
        <div class="box">
          <h2>The Moon Door</h2>
          <p>The door creaks, but does not open.</p>
          <p>"Common guests do not command the Moon Door."</p>
        </div>
        """ + ARRYN_FOOT)
        resp.set_cookie("rank", "guest")
        return resp

    return ARRYN_HEAD + f"""
    <div class="box">
      <h2>The Moon Door Swings Open</h2>
      <p>You speak as Lord of the Eyrie. The wind howls below.</p>
      <p><strong>Flag 3:</strong> {FLAG3}</p>
      <p>Hint: the Falcon's Crown awaits at
         <code>/falcon-crown?key=...</code></p>
    </div>
    """ + ARRYN_FOOT

# ---------- Stage 4: The Falcon's Crown ----------
@app.route("/falcon-crown")
def falcon_crown():
    if request.args.get("key") != FLAG3:
        return ARRYN_HEAD + """
        <div class="box">
          <h2>The Falcon's Crown</h2>
          <p>"The Crown bows to no stranger."</p>
        </div>
        """ + ARRYN_FOOT
    return ARRYN_HEAD + f"""
    <div class="box">
      <h2>👑 The Falcon's Crown 👑</h2>
      <p>The crown of the Kings of Mountain and Vale rests before you.</p>
      <p><strong>Final Flag:</strong> {FLAG4}</p>
      <p class="motto">"As High as Honor."</p>
    </div>
    """ + ARRYN_FOOT

# ---------- Optional nudge ----------
@app.route("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /bloody-gate\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)