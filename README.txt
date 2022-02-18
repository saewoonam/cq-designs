Title: Cryostat cq-designs 

Description:  

Code to generate CAD for the 4K, 40K plates, top collar, and cryoloom heat sinking clamp.  

Assembly of components above with the CryoMech PT405  & CRCMD-002. 

Code to generate hole callout for CAD 


+++To Generate CAD files+++ 

1. Install CadQuery 

https://github.com/CadQuery/CQ-editor#installation 

2. Open Files Required:
	collar_v2.py
	plate4k.py
	plate40k.py
	pt405_Block_Off_Plate.py (required for leak checking collar without using PT405) 
3. To export CAD.step files remove the comments ' """ ' triple quotations around exporters functions (includes defining varaible and show object). Example code seen below

	Ex: 	p = plate4K() 

    		show_object(p,options={"alpha":0.5, "color": (64, 164, 223)}) 

    		cq.exporters.export(p, './outputs/plate4K.step') 

4. The generate CAD.step files are located within the outputs folder. 


+++To Generate SVG Hole Callouts+++ 

SVG Holecallouts are generated with the JavaScript files located in "cq-designs\svgjs" folder. 
Files required for CAD fabrication:
	collar_top.js
	collar_bottom.js
	collar_face.js
	plate_4k.js
	plate40k.js
	PT405_Block_off.js

To Edit JavaScript files with realtime view updates

*Run PowerShell / command window as Administrator if on Windows*

1. Install nvm [https://github.com/nvm-sh/nvm]

2. Install Node LTS
	PowerShell Example: " nvm use lts "

3. Enable corepack
	PowerShell Example: " corepack enable "

4. Install stable version of Yarn (may require a changhe in exuction policy if using Windows PowerShell, Use "  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted " )

5. CD to cq-designs\svgjs directory

6. Start yarn nodemon with selected JavaScript file
	PowerShell Example: " yarn nodemon palte4K.js "

7. Open new Command Window (Ex. PowerShell)

8. CD to cq-designs\svgjs

9. Start Yarn Live server
	PowerShell Example: " yarn live-server "

10. A web browser window should pop. Select the chosen SVG file to edit. 


11. Changes made to the respective JavaScript file should be seen in the WebBrowser. 



Things Left to Fix:
	Design Cryoloom clamp in CQ
	Create Hole callout for ISO320 Blank Mod


