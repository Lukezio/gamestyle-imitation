import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET


#continue here
def write_xml(folder, img, bounding_boxes, savedir):
    if not os.path.isdir(savedir):
        os.mkdir(savedir)

    image = cv2.imread(img.path)
    height, width, depth = image.shape

    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = folder
    ET.SubElement(annotation, 'filename').text = img.name
    ET.SubElement(annotation, 'segmented').text = '0'
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)
    for bounding_box in bounding_boxes:
        ob = ET.SubElement(annotation, 'object')
        ET.SubElement(ob, 'name').text = bounding_box.label
        ET.SubElement(ob, 'pose').text = 'Unspecified'
        ET.SubElement(ob, 'truncated').text = '0'
        ET.SubElement(ob, 'difficult').text = '0'
        bbox = ET.SubElement(ob, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(bounding_box.top_left.x_coordinate)
        ET.SubElement(bbox, 'ymin').text = str(bounding_box.top_left.y_coordinate)
        ET.SubElement(bbox, 'xmax').text = str(bounding_box.bottom_right.x_coordinate)
        ET.SubElement(bbox, 'ymax').text = str(bounding_box.bottom_right.y_coordinate)

    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print=True)
    save_path = os.path.join(savedir, img.name.replace('png', 'xml'))
    with open(save_path, 'wb') as temp_xml:
        temp_xml.write(xml_str)


if __name__ == '__main__':
    """
    for testing
    """

    folder = 'images'
    img = [im for im in os.scandir('images') if '000001' in im.name][0]
    objects = ['fidget_spinner']
    tl = [(10, 10)]
    br = [(100, 100)]
    savedir = 'annotations'
    write_xml(folder, img, objects, savedir)