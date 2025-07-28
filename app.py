from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def form():
   return render_template('form.html')
@app.route('/generate', methods=['POST'])
def generate():
   customer_name = request.form['customer_name']
   vrf_name = request.form['vrf_name']
   tunnel_ip = request.form['tunnel_ip']
   remote_ip = request.form['remote_ip']
   local_subnet = request.form['local_subnet']
   remote_subnet = request.form['remote_subnet']
   config = f"""
   crypto isakmp policy 10
    encr aes
    hash sha256
    authentication pre-share
    group 14
   !
   crypto isakmp key cisco123 address {remote_ip}
   !
   crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac
   !
   crypto map VPN-MAP 10 ipsec-isakmp
    set peer {remote_ip}
    set transform-set VPN-SET
    match address 101
   !
   access-list 101 permit ip {local_subnet} {remote_subnet}
   !
   interface Tunnel0
    ip address {tunnel_ip}
    tunnel source GigabitEthernet0/0
    tunnel destination {remote_ip}
   !
   ip vrf {vrf_name}
    rd 65000:45
   !
   """
   return render_template("config.html", config=config)
if __name__ == '__main__':
   app.run(debug=True)
