# Burp_Addons
Some custom burp extension scripts i thought i'd share. Nothing amazing but sometimes useful.

Mixed Case Iterator
-------------------
This script is a simple intruder payload extention which takes the selected value in intruder and iterates through all possible combinations of case.  This might come in handy if you wanted to check all combinations of a particular word for WAF/custom filtering issues. 

To use, highlight the word in the request that you wish to iterate the case for and in the payloads tab, select extension generated. Then via the Select Generator button choose the addon in the list. The highlighted word will automatically be picked up and a list of payloads generated when you click Start Attack.

I've given it a basic test and it seems to work OK but with long words or phrases it'll generate more and more payloads for intruder to use. For example, a highlighted area with 8 characters will generate 256 payloads, 9 characters and it's 512 and so on.

Anything not A-Z is left alone and it should be ok to leave in special charcters but I only gave this a quick test, there may be some bugs
