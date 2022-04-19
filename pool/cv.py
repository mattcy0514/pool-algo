import cv2
import numpy as np
import matplotlib.pyplot as plt
import json

# width, height = 254, 508 #127*2,254*2(全球台)

width, height = 254, 222 #127*2,111*2(寬短邊，長)

pos_dict = {}

def create_table():
    # new generated img
    img = np.zeros((height, width, 3), dtype=np.uint8)  # create 2D table image
    img[:, :] = [0, 120, 255]  # setting RGB colors to green pool table color, (0,180,10)=certain green,blue
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # # create circle in the right size
    # cv2.circle(img, (int(width / 2), int(height / 5)),  # center of circle
    #            int((width / 3) / 2),  # radius
    #            (50, 255, 50))  # color

    # delete half of circle by coloring in green color
    # img[int(height / 5):height, 0:width] = [0, 120, 255]
    # create line
    # cv2.line(img, (0, int(height / 5)), (width, int(height / 5)), (50, 255, 50))

    return img

def draw_holes(input_img, color3=(200, 140, 0)):
    color = (190, 190, 190)  # gray color
    color2 = (120, 120, 120)  # gray color, for circles (holes) on generated img

    img = input_img.copy()  # make a copy of input image

    # borders
    # cv2.line(img, (0, 0), (width, 0), color3, 3)  # top
    # cv2.line(img, (0, height), (width, height), color3, 3)  # bot
    # cv2.line(img, (0, 0), (0, height), color3, 3)  # left
    # cv2.line(img, (width, 0), (width, height), color3, 3)  # right

    # # adding circles to represent holes on table
    # cv2.circle(img, (0, 0), 11, color, -1)  # top right
    # cv2.circle(img, (width, 0), 11, color, -1)  # top left
    # cv2.circle(img, (0, height), 11, color, -1)  # bot left
    # cv2.circle(img, (width, height), 11, color, -1)  # bot right
    # cv2.circle(img, (width, int(height / 2)), 8, color, -1)  # mid right
    # cv2.circle(img, (0, int(height / 2)), 8, color, -1)  # mid left
    #
    # # adding another, smaller circles to the previous ones
    # cv2.circle(img, (0, 0), 9, color2, -1)  # top right
    # cv2.circle(img, (width, 0), 9, color2, -1)  # top left
    # cv2.circle(img, (0, height), 9, color2, -1)  # bot left
    # cv2.circle(img, (width, height), 9, color2, -1)  # bot right
    # cv2.circle(img, (width, int(height / 2)), 6, color2, -1)  # mid right
    # cv2.circle(img, (0, int(height / 2)), 6, color2, -1)  # mid left

    return img

def draw_balls(ctrs, background=create_table(), radius=7, size=-1, img=0):#radius=7, size=-1, img=0
    K = np.ones((3, 3), np.uint8)  # filter

    final = background.copy()  # canvas
    mask = np.zeros((222, 254), np.uint8)  # empty image, same size as 2d generated final output

    for x in range(len(ctrs)):  # for all contours

        # find center of contour
        M = cv2.moments(ctrs[x])
        cX = int(M['m10'] / M['m00'])  # X pos of contour center
        cY = int(M['m01'] / M['m00'])  # Y pos

        # find color average inside contour
        mask[...] = 0  # reset the mask for every ball
        cv2.drawContours(mask, ctrs, x, 255, -1)  # draws mask for each contour
        mask = cv2.erode(mask, K, iterations=3)  # erode mask several times to filter green color around balls contours

        # balls design:

        # circle to represent snooker ball
        final = cv2.circle(final,  # img to draw on
                           (cX, cY),  # position on img
                           radius,  # radius of circle - size of drawn snooker ball
                           cv2.mean(img, mask),
                           # color mean of each contour-color of each ball (src_img=transformed img)
                           size)  # -1 to fill ball with color

        # add black color around the drawn ball (for cosmetics)
        # final = cv2.circle(final, (cX, cY), radius, 0, 1)

        # small circle for light reflection
        # final = cv2.circle(final, (cX - 2, cY - 2), 2, (255, 255, 255), -1)

    return final

def draw_rectangles(ctrs, img):
    output = img.copy()

    for i in range(len(ctrs)):
        M = cv2.moments(ctrs[i])  # moments
        rot_rect = cv2.minAreaRect(ctrs[i])
        w = rot_rect[1][0]  # width
        h = rot_rect[1][1]  # height

        box = np.int64(cv2.boxPoints(rot_rect))
        cv2.drawContours(output, [box], 0, (255, 100, 0), 2)  # draws box

    return output

def find_ctrs_color(ctrs, input_img):
    K = np.ones((3, 3), np.uint8)  # filter
    output = input_img.copy()  # np.zeros(input_img.shape,np.uint8) # empty img
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)  # gray version
    mask = np.zeros(gray.shape, np.uint8)  # empty mask

    for i in range(len(ctrs)):  # for all contours

        # find center of contour
        M = cv2.moments(ctrs[i])
        cX = int(M['m10'] / M['m00'])  # X pos of contour center
        cY = int(M['m01'] / M['m00'])  # Y pos
        # print([cX,cY])

        mask[...] = 0  # reset the mask for every ball

        cv2.drawContours(mask, ctrs, i, 255,
                         -1)  # draws the mask of current contour (every ball is getting masked each iteration)

        mask = cv2.erode(mask, K, iterations=3)  # erode mask to filter green color around the balls contours

        output = cv2.circle(output,  # img to draw on
                            (cX, cY),  # position on img
                            20,  # radius of circle - size of drawn snooker ball
                            cv2.mean(input_img, mask),#mask
                            # color mean of each contour-color of each ball (src_img=transformed img)
                            -1)  # -1 to fill ball with color
    return output

def filter_ctrs(ctrs, min_s=90, max_s=358, alpha=3.445): #min_s=0, max_s=800, alpha=3.445
    filtered_ctrs = []  # list for filtered contours
    for x in range(len(ctrs)):  # for all contours

        rot_rect = cv2.minAreaRect(ctrs[x])  # area of rectangle around contour
        w = rot_rect[1][0]  # width of rectangle
        h = rot_rect[1][1]  # height
        area = cv2.contourArea(ctrs[x])  # contour area

        if (h * alpha < w) or (w * alpha < h):  # if the contour isnt the size of a snooker ball
            continue  # do nothing

        if (area < min_s) or (area > max_s):  # if the contour area is too big/small
            continue  # do nothing

        # if it failed previous statements then it is most likely a ball
        filtered_ctrs.append(ctrs[x])  # add contour to filtered cntrs list
    return filtered_ctrs  # returns filtere contours

def main():
    img = cv2.imread('pass2.jpeg')




    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
    parameters = cv2.aruco.DetectorParameters_create()

    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(img, dictionary, parameters=parameters)
    img = cv2.aruco.drawDetectedMarkers(img, markerCorners, markerIds)

    if markerIds is not None and len(markerIds) >= 4:
        # for every tag in the array of detected tags...
        # pts1 = [None] * 4
        for i in range(1, len(markerIds) + 1):
            C1 = np.float32(markerIds)
            if i in markerIds:  #掃到的QR碼順序:例如2,4,3,1
                if (int(C1[i-1]) == 1):
                    corner1 = markerCorners[i-1][0][1]
                if (int(C1[i-1]) == 2):
                    corner2 = markerCorners[i-1][0][0]  #[0][0][0]左上
                if (int(C1[i-1]) == 3):
                    corner3 = markerCorners[i-1][0][2]
                if (int(C1[i-1]) == 4):
                    corner4 = markerCorners[i-1][0][3]



        if len(markerIds) >= 4:
            pts1 = np.float32([corner1,corner2, corner3, corner4])
            pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            transformed = cv2.warpPerspective(img,matrix,(width, height))
            cv2.imshow("PerspectiveTransform", transformed)

            transformed_blur = cv2.GaussianBlur(transformed,(0,0),2) # blur applied
            blur_RGB = cv2.cvtColor(transformed_blur, cv2.COLOR_BGR2RGB) # rgb version

            # hsv colors of the snooker table
            lower = np.array([97,100,117])#HSV blue
            upper = np.array([117,255,255]) # HSV of snooker green: (60-70, 200-255, 150-240)

            hsv = cv2.cvtColor(blur_RGB, cv2.COLOR_RGB2HSV) # convert to hsv
            mask = cv2.inRange(hsv, lower, upper) # table's mask

            # apply closing
            kernel = np.ones((5,5),np.uint8)
            mask_closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) # dilate->erode

            # invert mask to focus on objects on table
            _,mask_inv = cv2.threshold(mask_closing,5,255,cv2.THRESH_BINARY_INV) # mask inv

            masked_img = cv2.bitwise_and(transformed, transformed, mask=mask_inv) # masked image with inverted mask

            # cv2.imshow("1",transformed_blur)
            # cv2.imshow("2",mask_closing)
            # cv2.imshow("3",masked_img)

            # find contours and filter them
            ctrs, hierarchy = cv2.findContours(mask_inv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # create contours in filtered img

            # draw contours before filter
            detected_objects = draw_rectangles(ctrs, transformed) # detected objects will be marked in boxes

            ctrs_filtered = filter_ctrs(ctrs) # filter unwanted contours (wrong size or shape)

            # draw contours after filter
            detected_objects_filtered = draw_rectangles(ctrs_filtered, transformed) # filtered detected objects will be marked in boxes

            # find average color inside contours:
            ctrs_color = find_ctrs_color(ctrs_filtered, transformed)
            ctrs_color = cv2.addWeighted(ctrs_color,0.5,transformed,0.5,0) # contours color image + transformed image

            # cv2.imshow("4",detected_objects)
            # cv2.imshow("5",detected_objects_filtered)
            # cv2.imshow("6",ctrs_color)

            # design of the 2D generated table
            final = draw_balls(ctrs_filtered, img=transformed)  # gets contours and draws balls in their centers
            final = draw_holes(final)  # draws holes in the 2D img

            cv2.imshow("7", final)
            #
            lower_range_red = np.array([169, 100, 100])
            upper_range_red = np.array([189, 255, 255])
            lower_range_bla = np.array([0, 0, 0])
            upper_range_bla = np.array([180, 255, 70 ])
            lower_range_y = np.array([11, 43, 46])
            upper_range_y = np.array([25, 255, 255])
            lower_range_g = np.array([66, 122, 80])
            upper_range_g = np.array([90, 255, 255])
            lower_range_w = np.array([0, 0, 231])
            upper_range_w = np.array([180, 50, 255])
            lower_range_or = np.array([0, 80, 120])
            upper_range_or = np.array([20, 255, 255])

            lower_range_test = np.array([0, 0, 221])
            upper_range_test = np.array([180, 30, 255])

            hsv1 = cv2.cvtColor(final, cv2.COLOR_BGR2HSV)

            mask_red = cv2.inRange(hsv1, lower_range_red, upper_range_red)
            mask_bla = cv2.inRange(hsv1, lower_range_bla, upper_range_bla)
            mask_y = cv2.inRange(hsv1, lower_range_y, upper_range_y)
            mask_g = cv2.inRange(hsv1, lower_range_g, upper_range_g)
            mask_w = cv2.inRange(hsv1, lower_range_w, upper_range_w)
            mask_or = cv2.inRange(hsv1, lower_range_or, upper_range_or)

            mask_test = cv2.inRange(hsv1, lower_range_test, upper_range_test)

            # cv2.imshow("RED", mask_red)
            # cv2.imshow("BLACK",mask_bla)
            # cv2.imshow("YELLOW",mask_y)
            # cv2.imshow("Green", mask_g)
            # cv2.imshow("WHITE", mask_w)
            # cv2.imshow("ORANGE", mask_or)

            # cv2.imshow("TEST", mask_test)


            #白球(母球)
            contours, hierarchy = cv2.findContours(image=mask_w, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            image_copy = mask_w.copy()
            cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,lineType=cv2.LINE_AA)
            ret, thresh = cv2.threshold(mask_w, 127, 255, 0)
            M = cv2.moments(thresh)
            if not (M["m00"]==0):
                cX1 = int(M["m10"] / M["m00"])
                cY1 = int(M["m01"] / M["m00"])
                pos_dict["{}".format(0)] = [[cX1], [cY1]]

            #黃球(1號)
            contours, hierarchy = cv2.findContours(image=mask_y, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            image_copy = mask_w.copy()
            cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                            lineType=cv2.LINE_AA)
            ret, thresh = cv2.threshold(mask_y, 127, 255, 0)
            M = cv2.moments(thresh)
            if not(M["m00"] == 0):
                cX1 = int(M["m10"] / M["m00"])
                cY1 = int(M["m01"] / M["m00"])
                pos_dict["{}".format(1)] = [[cX1], [cY1]]

            # 紅球(3號)
            contours, hierarchy = cv2.findContours(image=mask_red, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            image_copy = mask_w.copy()
            cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                                lineType=cv2.LINE_AA)
            ret, thresh = cv2.threshold(mask_red, 127, 255, 0)
            M = cv2.moments(thresh)
            if not(M["m00"] == 0):
                cX1 = int(M["m10"] / M["m00"])
                cY1 = int(M["m01"] / M["m00"])
                pos_dict["{}".format(3)] = [[cX1], [cY1]]

            # 橘球(5號)
            contours, hierarchy = cv2.findContours(image=mask_or, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            image_copy = mask_w.copy()
            cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                            lineType=cv2.LINE_AA)
            ret, thresh = cv2.threshold(mask_or, 127, 255, 0)
            M = cv2.moments(thresh)
            if not(M["m00"] == 0):
                cX1 = int(M["m10"] / M["m00"])
                cY1 = int(M["m01"] / M["m00"])
                pos_dict["{}".format(5)] = [[cX1], [cY1]]

            # 綠球(6號)
            contours, hierarchy = cv2.findContours(image=mask_g, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            image_copy = mask_w.copy()
            cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                            lineType=cv2.LINE_AA)
            ret, thresh = cv2.threshold(mask_g, 127, 255, 0)
            M = cv2.moments(thresh)
            if not(M["m00"] == 0):
                cX1 = int(M["m10"] / M["m00"])
                cY1 = int(M["m01"] / M["m00"])
                pos_dict["{}".format(6)] = [[cX1], [cY1]]

            # 黑球(8號)
            contours, hierarchy = cv2.findContours(image=mask_bla, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            image_copy = mask_w.copy()
            cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                            lineType=cv2.LINE_AA)
            ret, thresh = cv2.threshold(mask_bla, 127, 255, 0)
            M = cv2.moments(thresh)
            if not(M["m00"] == 0):
                cX1 = int(M["m10"] / M["m00"])
                cY1 = int(M["m01"] / M["m00"])
                pos_dict["{}".format(8)] = [[cX1], [cY1]]

            # 測試球(沒有球)
            contours, hierarchy = cv2.findContours(image=mask_test, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            image_copy = mask_w.copy()
            cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                            lineType=cv2.LINE_AA)
            ret, thresh = cv2.threshold(mask_test, 127, 255, 0)
            M = cv2.moments(thresh)
            if not (M["m00"] == 0):
                cX1 = int(M["m10"] / M["m00"])
                cY1 = int(M["m01"] / M["m00"])
                pos_dict["{}".format(9)] = [[cX1], [cY1]]
   
    return json.dumps(pos_dict)

    # cv2.waitKey(0)

print(main())