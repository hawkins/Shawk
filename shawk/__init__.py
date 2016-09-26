"""Define the shawk module"""

import re

GATEWAY_REGEX = re.compile("(.*)@(txt.bell.ca|\
sms.3rivers.net|\
paging.acswireless.com|\
txt.att.net|\
message.alltel.com|\
bplmobile.com|\
txt.bellmobility.ca|\
txt.bell.ca|\
txt.bellmobility.ca|\
blueskyfrog.com|\
sms.bluecell.com|\
myboostmobile.com|\
mobile.celloneusa.com|\
csouth1.com|\
cwemail.com|\
messaging.centurytel.net|\
rpgmail.net|\
airtelchennai.com|\
txt.att.net|\
msg.clearnet.com|\
comcastpcs.textmsg.com|\
sms.comviq.se|\
corrwireless.net|\
t-mobile-sms.de|\
airtelmail.com|\
delhi.hutch.co.in|\
mobile.dobson.net|\
sms.orange.nl|\
sms.emt.ee|\
sms.edgewireless.com|\
escotelmobile.com|\
fido.ca|\
t-mobile-sms.de|\
bplmobile.com|\
sms.goldentele.com|\
celforce.com|\
messaging.sprintpcs.com|\
text.houstoncellular.net|\
ideacellular.net|\
ivctext.com|\
inlandlink.com|\
pinjsmtel.com|\
escotelmobile.com|\
airtelkol.com|\
smsmail.lmt.lv|\
smsmail.lmt.lv|\
pagemci.com|\
text.mtsmobility.com|\
bplmobile.com|\
ideacellular.net|\
text.mtsmobility.com|\
mymeteor.ie|\
mymetropcs.com|\
m1.com.sg|\
fido.ca|\
clearlydigital.com|\
mobilecomm.net|\
m1.com.sg|\
page.mobilfone.com|\
ml.bm|\
mobistar.be|\
sms.co.tz|\
mobtel.co.yu|\
correo.movistar.net|\
bplmobile.com|\
sms.netcom.no|\
messaging.nextel.com|\
pcs.ntelos.com|\
mmail.co.uk|\
o2imail.co.uk|\
onemail.at|\
onlinebeep.net|\
optusmobile.com.au|\
orangemail.co.in|\
sms.orange.nl|\
orange.net|\
mujoskar.cz|\
sms.luxgsm.lu|\
pcsone.net|\
bplmobile.com|\
sms.primtel.ru|\
msg.fi.google.com|\
sms.pscel.com|\
qwestmp.com|\
pcs.rogers.com|\
pcs.rogers.com|\
scs-900.ru|\
sfr.fr|\
safaricomsms.com|\
satelindogsm.com|\
text.simplefreedom.net|\
mysmart.mymobile.ph|\
txt.bell.ca|\
page.southernlinc.com|\
email.swbw.com|\
messaging.sprintpcs.com|\
tms.suncom.com|\
mysunrise.ch|\
mobile.surewest.com|\
freesurf.ch|\
bluewin.ch|\
sms.t-mobile.at|\
t-d1-sms.de|\
t-mobile.uk.net|\
tmomail.net|\
timnet.com|\
bplmobile.com|\
sms.tele2.lv|\
movistar.net|\
mobilpost.no|\
gsm1800.telia.dk|\
msg.telus.com|\
txt.att.net|\
tms.suncom.com|\
sms.umc.com.ua|\
email.uscc.net|\
uswestdatamail.com|\
utext.com|\
sms.uraltel.ru|\
escotelmobile.com|\
vtext.com|\
vmobile.ca|\
vmobl.com|\
sms.vodafone.it|\
c.vodafone.ne.jp|\
vodafone.net|\
sms.wcc.net|\
cellularonewest.com|\
wyndtell.com)")

GATEWAYS = {
    "President's Choice": 'txt.bell.ca',
    '3 River Wireless': 'sms.3rivers.net',
    'ACS Wireless': 'paging.acswireless.com',
    'AT&T': 'txt.att.net',
    'Alltel': 'message.alltel.com',
    'BPL Mobile': 'bplmobile.com',
    'Bell Canada': 'txt.bellmobility.ca',
    'Bell Mobility (Canada)': 'txt.bell.ca',
    'Bell Mobility': 'txt.bellmobility.ca',
    'Blue Sky Frog': 'blueskyfrog.com',
    'Bluegrass Cellular': 'sms.bluecell.com',
    'Boost Mobile': 'myboostmobile.com',
    'Cellular One': 'mobile.celloneusa.com',
    'Cellular South': 'csouth1.com',
    'Centennial Wireless': 'cwemail.com',
    'CenturyTel': 'messaging.centurytel.net',
    'Chennai RPG Cellular': 'rpgmail.net',
    'Chennai Skycell / Airtel': 'airtelchennai.com',
    'Cingular': 'txt.att.net',
    'Clearnet': 'msg.clearnet.com',
    'Comcast': 'comcastpcs.textmsg.com',
    'Comviq': 'sms.comviq.se',
    'Corr Wireless Communications': 'corrwireless.net',
    'DT T-Mobile': 't-mobile-sms.de',
    'Delhi Aritel': 'airtelmail.com',
    'Delhi Hutch': 'delhi.hutch.co.in',
    'Dobson': 'mobile.dobson.net',
    'Dutchtone / Orange-NL': 'sms.orange.nl',
    'EMT': 'sms.emt.ee',
    'Edge Wireless': 'sms.edgewireless.com',
    'Escotel': 'escotelmobile.com',
    'Fido': 'fido.ca',
    'German T-Mobile': 't-mobile-sms.de',
    'Goa BPLMobil': 'bplmobile.com',
    'Golden Telecom': 'sms.goldentele.com',
    'Gujarat Celforce': 'celforce.com',
    'Helio': 'messaging.sprintpcs.com',
    'Houston Cellular': 'text.houstoncellular.net',
    'Idea Cellular': 'ideacellular.net',
    'Illinois Valley Cellular': 'ivctext.com',
    'Inland Cellular Telephone': 'inlandlink.com',
    'JSM Tele-Page': 'pinjsmtel.com',
    'Kerala Escotel': 'escotelmobile.com',
    'Kolkata Airtel': 'airtelkol.com',
    'Kyivstar': 'smsmail.lmt.lv',
    'LMT': 'smsmail.lmt.lv',
    'MCI': 'pagemci.com',
    'MTS': 'text.mtsmobility.com',
    'Maharashtra BPL Mobile': 'bplmobile.com',
    'Maharashtra Idea Cellular': 'ideacellular.net',
    'Manitoba Telecom Systems': 'text.mtsmobility.com',
    'Meteor': 'mymeteor.ie',
    'Metro PCS': 'mymetropcs.com',
    'MiWorld': 'm1.com.sg',
    'Microcell': 'fido.ca',
    'Midwest Wireless': 'clearlydigital.com',
    'Mobilcomm': 'mobilecomm.net',
    'Mobileone': 'm1.com.sg',
    'Mobilfone': 'page.mobilfone.com',
    'Mobility Bermuda': 'ml.bm',
    'Mobistar Belgium': 'mobistar.be',
    'Mobitel Tanzania': 'sms.co.tz',
    'Mobtel Srbija': 'mobtel.co.yu',
    'Movistar': 'correo.movistar.net',
    'Mumbai BPL Mobile': 'bplmobile.com',
    'Netcom': 'sms.netcom.no',
    'Nextel': 'messaging.nextel.com',
    'Ntelos': 'pcs.ntelos.com',
    'O2 (M-mail)': 'mmail.co.uk',
    'O2': 'o2imail.co.uk',
    'One Connect Austria': 'onemail.at',
    'OnlineBeep': 'onlinebeep.net',
    'Optus Mobile': 'optusmobile.com.au',
    'Orange Mumbai': 'orangemail.co.in',
    'Orange NL / Dutchtone': 'sms.orange.nl',
    'Orange': 'orange.net',
    'Oskar': 'mujoskar.cz',
    'P&T Luxembourg': 'sms.luxgsm.lu',
    'PCS One': 'pcsone.net',
    'Pondicherry BPL Mobile': 'bplmobile.com',
    'Primtel': 'sms.primtel.ru',
    'Project Fi': 'msg.fi.google.com',
    'Public Service Cellular': 'sms.pscel.com',
    'Qwest': 'qwestmp.com',
    'Rogers AT&T Wireless': 'pcs.rogers.com',
    'Rogers Canada': 'pcs.rogers.com',
    'SCS-900': 'scs-900.ru',
    'SFR France': 'sfr.fr',
    'Safaricom': 'safaricomsms.com',
    'Satelindo GSM': 'satelindogsm.com',
    'Simple Freedom': 'text.simplefreedom.net',
    'Smart Telecom': 'mysmart.mymobile.ph',
    'Solo Mobile': 'txt.bell.ca',
    'Southern LINC': 'page.southernlinc.com',
    'Southwestern Bell': 'email.swbw.com',
    'Sprint': 'messaging.sprintpcs.com',
    'Sumcom': 'tms.suncom.com',
    'Sunrise Mobile': 'mysunrise.ch',
    'Surewest Communicaitons': 'mobile.surewest.com',
    'Surewest Communications': 'freesurf.ch',
    'Swisscom': 'bluewin.ch',
    'T-Mobile Austria': 'sms.t-mobile.at',
    'T-Mobile Germany': 't-d1-sms.de',
    'T-Mobile UK': 't-mobile.uk.net',
    'T-Mobile': 'tmomail.net',
    'TIM': 'timnet.com',
    'Tamil Nadu BPL Mobile': 'bplmobile.com',
    'Tele2 Latvia': 'sms.tele2.lv',
    'Telefonica Movistar': 'movistar.net',
    'Telenor': 'mobilpost.no',
    'Telia Denmark': 'gsm1800.telia.dk',
    'Telus': 'msg.telus.com',
    'Tracfone': 'txt.att.net',
    'Triton': 'tms.suncom.com',
    'UMC': 'sms.umc.com.ua',
    'US Cellular': 'email.uscc.net',
    'US West': 'uswestdatamail.com',
    'Unicel': 'utext.com',
    'Uraltel': 'sms.uraltel.ru',
    'Uttar Pradesh Escotel': 'escotelmobile.com',
    'Verizon': 'vtext.com',
    'Virgin Mobile Canada': 'vmobile.ca',
    'Virgin Mobile': 'vmobl.com',
    'Vodafone Italy': 'sms.vodafone.it',
    'Vodafone Japan': 'c.vodafone.ne.jp',
    'Vodafone UK': 'vodafone.net',
    'West Central Wireless': 'sms.wcc.net',
    'Western Wireless': 'cellularonewest.com',
    'Wyndtell': 'wyndtell.com'
}

from shawk.Client import Client
from shawk.Contact import Contact
from shawk.Message import Message

__name__ = "shawk"
