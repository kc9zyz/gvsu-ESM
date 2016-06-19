import esmSerial
import esmDCLoad
import esmPrint
import esmWebInterface

def serCallback(byte):
    print(str(byte,'ascii'), end="")
output = (False,200)
dc = esmDCLoad.esmDCLoad()
serPorts = [(esmSerial.esmSerialPorts.electronicLoad,"/dev/tty.usbserial",dc.getCallback(),38400)]
p = esmPrint.esmPrint(False)
s = esmSerial.esmSerial(p,serPorts)
output = dc.trackMPPT(s,p,9000)
s.close()

print('OUTPUT '+str(int(output[1])))
output = (False,1)

dataPoint = esmWebInterface.esmDataPoint()
dataPoint.output = int(output[1])

webInterface = esmWebInterface.esmWebInterface('http://cis.gvsu.edu/~neusonw/solar/data/',b'AAAAB3NzaC1yc2EAAAADAQABAAABAQD9KNADbe8h+5ZZnT/mggSUPxvkmEmlT1rWJqwK4DdIb4d19HPUKu8OIhouYz4RepmBs3G3/JXRfDKGpSeNOYlOeXhUe8MRffXfV2ZaP819gqiuFha9wsvyWXLfO9f/GNfmAuc8r4FCfP4A77l/FU9tpT+fOxeP6al08iJ5Ua1fMFGf3hhqnpixanLgyylFD+pPjX6KXqczICUDTWwGmmsgyLTyUEmmUN4sW7WZc4fNaGQSKidsDDzMLE7dFbDVY8F/to//bihpI4UmLwJYK8D/S2OcvK3skgqLDJ5K1FWhHCzNIrcp9KVxx3Na2XgrukJzhU0eHHASuPfcYElKHK/v')

webInterface.sendUpdate(dataPoint)



