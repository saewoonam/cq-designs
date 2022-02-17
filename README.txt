Title: Cryostat cq-designs 

Description:  

Code to generate CAD for the 4K, 40K plates, top collar, and cryoloom heat sinking clamp.  

Assembly of components above with the CryoMech PT405  & CRCMD-002. 

Code to generate hole callout for CAD 


+++To Generate CAD files+++ 

1. Install CadQuery 

https://github.com/CadQuery/CQ-editor#installation 

2. Open CAD.py File 

3. To export CAD.step files remove the comments ' """ ' triple quotations around exporters functions (includes defining varaible and show object). Example code seen below 

	Ex: 	p = plate4K() 

    		show_object(p,options={"alpha":0.5, "color": (64, 164, 223)}) 

    		cq.exporters.export(p, './outputs/plate4K.step') 

4. The generate CAD.step is located within the outputs folder. 


+++To Generate SVG Hole Callouts+++ 

1. 