import gnodeclient
import odml
s = odml.Section(name='xxx')
p = odml.Property(name='FrequenciesUsed', value=[10,20,30])
ss = gnodeclient.session.create(location="http://predata.g-node.org", username="bob", password="pass")
s = ss.set(s)
s.append(p)
p = ss.set(p)
