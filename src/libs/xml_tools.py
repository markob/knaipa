import logging

from xml.dom import minidom


def genStringNode(dom, str, name):
    root = dom.createElement(name)

    text = dom.createTextNode(str)
    root.appendChild(text)

    return root


def genDateNode(dom, date, name='date'):
    root = dom.createElement(name)

    node = dom.createElement('year')
    root.appendChild(node)
    text = dom.createTextNode(str(date.year))
    node.appendChild(text)

    node = dom.createElement('month')
    root.appendChild(node)
    text = dom.createTextNode(str(date.month))
    node.appendChild(text)
    node = dom.createElement('day')
    root.appendChild(node)
    text = dom.createTextNode(str(date.day))
    node.appendChild(text)

    return root
    
    
def genTimeNode(dom, time, name='time'):
    root = dom.createElement(name)

    node = dom.createElement('hour')
    root.appendChild(node)
    text = dom.createTextNode(str(time.hour))
    node.appendChild(text)

    node = dom.createElement('minute')
    root.appendChild(node)
    text = dom.createTextNode(str(time.minute))
    node.appendChild(text)

    node = dom.createElement('second')
    root.appendChild(node)
    text = dom.createTextNode(str(time.day))
    node.appendChild(text)

    return root


def genDateTimeNode(dom, datetime, name='datetime'):
    root = genDateNode(dom, datetime, name)

    node = dom.createElement('hour')
    root.appendChild(node)
    text = dom.createTextNode(str(datetime.hour))
    node.appendChild(text)

    node = dom.createElement('minute')
    root.appendChild(node)
    text = dom.createTextNode(str(datetime.minute))
    node.appendChild(text)

    node = dom.createElement('second')
    root.appendChild(node)
    text = dom.createTextNode(str(datetime.day))
    node.appendChild(text)

    return root


def genTextNode(dom, text, name='text'):
    root = dom.createElement(name)

    node = dom.createCDATASection(text)
    root.appendChild(node)

    return root


def createXmlDoc(rootName):
    xmlDoc = minidom.Document()

    root = xmlDoc.createElement(rootName)
    xmlDoc.appendChild(root)

    return xmlDoc
