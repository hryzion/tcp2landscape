from PIL import Image, ImageDraw
import numpy as np
import math

GR = (2.23606797749979 - 1) / 2


def calculate_linear_function(point1, point2):
    """
    根据两个点的坐标计算对应的一次函数的斜率和截距

    参数:
    point1 (tuple): 第一个点的坐标，格式为 (x1, y1)
    point2 (tuple): 第二个点的坐标，格式为 (x2, y2)

    返回:
    tuple: 包含斜率 (k) 和截距 (b) 的元组
    """
    x1, y1 = point1
    x2, y2 = point2
    # 计算斜率k，根据两点间斜率公式 (y2 - y1) / (x2 - x1)
    if x2 - x1 == 0:
        raise ValueError("两点横坐标相同，无法构成一次函数（直线）")
    k = (y2 - y1) / (x2 - x1)
    # 计算截距b，将其中一个点坐标代入y = kx + b 求解b
    b = y1 - k * x1
    return k, b








def triangular_func(x,w=2,phi=0,A=100):
    return A * np.sin(w * x+phi)


def linear_function(k,b,x):
    return int(k*x+b)


def interval_overlap(a,b):
    
    if (a[1] < b[0] or a[0] > b[1]):
        return False
    if (a[1]<b[1] and a[0] > b[0]) or (a[1]>b[1] and a[0] < b[0]):
        return True
    r = [a[0],a[1],b[0],b[1]]
    r.sort()
    print(r)
    if (r[-1]- r[0])/(r[1]-r[2]) > 2:
        return False
    return True



def generate_line_segments(num_segments, num_samples, num_pulse):
    """
    生成指定数量的折线段
    """
    width = 1600
    height = 450
    left_point = (-200, 0.8*height)  # 起点（在图片左侧外面）
    right_point = (width + 200, 0)  # 终点（在图片右侧外面）
    mid_height = (left_point[1]+right_point[1])//2
    k,b = calculate_linear_function(left_point,right_point)
    print(k,b)
    image = Image.new('RGB', (width, height), 'white')

    draw = ImageDraw.Draw(image)
    # draw.line([left_point,right_point], fill='black', width=2)

    pulses = []
    for i in range(num_pulse):

        while True:
            start_point = np.random.uniform(0,width)
            om = np.random.uniform(0, 4)
            w = 1/50/(om+1)
            t =  2 * np.pi / w
            end_point = start_point + t /2

            flag = True
            for p in pulses:
                if interval_overlap(p,[start_point,end_point]):
                    print(p,[start_point,end_point])
                    flag = False
            if flag:
                pulses.append([start_point,end_point])
                break



        mid = (start_point+end_point) / 2
        phi = - w * start_point

        vr = np.random.normal(GR*height,50)
        A_range = vr
        A = np.random.uniform(A_range-100,A_range)

        x1 = np.random.uniform((start_point+mid)/2,mid)
        x2 = np.random.uniform(mid,(end_point+mid)/2)
        y1 = triangular_func(x1,w,phi+np.pi,A) + vr
        y2 = triangular_func(x2,w,phi+np.pi,A) + vr
        
        pts = [
            (int(start_point), height // 2+ vr),
            (int(x1),int(y1)),
            (int(x2),int(y2)),
            (int(end_point), height // 2+ vr)
        ]
        
        draw.line(pts,fill='black',width=2)

        pulse_pts = pts



    # 生成背景线
    background_pts = []
    for i in range(num_segments):
        start_point = left_point
        points = [start_point]
        current_point = [0,0]
        samples = 200
        x_step = width/samples
        x = 0
        pt=[]

        
        om = np.random.uniform(3, 6)
        w = 1/50/(om+1)
        t =  2 * np.pi / w
        round = (int(width / t)+1) * 4
        
        oa = np.random.uniform(0,3)

        phi = w * np.random.uniform(0,t)

        vr = np.random.normal((1-GR) * height, 50)
        

        x_n = -phi
        mid = 0
        pts = [start_point]


        for _ in range(round):
            mid = x_n + t / 4
            # x1 = np.random.normal((x_n+mid)/2,t/16)
            # x2 = np.random.normal((x_n+mid + t/2)/2,t/16)
            x1 = np.random.uniform(x_n, mid)
            x2 = np.random.uniform(mid,x_n+t/2)
            y1 = triangular_func(x1,w,phi=phi, A=50*oa) + vr
            y2 = triangular_func(x2,w, phi=phi, A=50*oa) + vr
            x_n += t / 2
            
            eps = np.random.uniform(0,1)
        
            if eps > 0:
                pts.append((x1,y1))
                pts.append((x2,y2))
                draw.line(pts,fill='blue',width=2)
          
            pts = [(x2,y2)]
        print(points)


    # 生成前景线
    foreground_pts = []
    for i in range(num_segments):
        start_point = left_point
        points = [start_point]
        current_point = [0,0]
        samples = 200
        x_step = width/samples
        x = 0
        pt=[]

        
        om = np.random.uniform(3, 6)
        w = 1/50/(om+1)
        t =  2 * np.pi / w
        round = (int(width / t)+1) * 4
        
        oa = np.random.uniform(1,2)

        phi = w * np.random.uniform(0,t)

        vr = np.random.normal( height, 30)
        

        x_n = -phi
        mid = 0
        pts = [start_point]


        for _ in range(round):
            mid = x_n + t / 4
            # x1 = np.random.normal((x_n+mid)/2,t/16)
            # x2 = np.random.normal((x_n+mid + t/2)/2,t/16)
            x1 = np.random.uniform(x_n, mid)
            x2 = np.random.uniform(mid,x_n+t/2)
            y1 = triangular_func(x1,w,phi=phi, A=50*oa) + vr
            y2 = triangular_func(x2,w, phi=phi, A=50*oa) + vr
            x_n += t / 2
            
            eps = np.random.uniform(0,1)
        
            if eps > 0:
                pts.append((x1,y1))
                pts.append((x2,y2))
                draw.line(pts,fill='green',width=2)
          
            pts = [(x2,y2)]


   
       

            
            
        print(points)



    return image, pulse_pts, background_pts, foreground_pts


def generate_perpendicular_tcp(num_flow,num_samples):
    width = 450
    height = 800
    up_point = (0,-200)  
    min_distance= 100
    image = Image.new('RGB', (width,height), 'white')
    draw = ImageDraw.Draw(image)

    down_point_xs =[]
    limit = 0
    while len(down_point_xs) < num_flow:
        limit+=1
        dpx = np.random.randint(100, 450)
        if not down_point_xs or all(abs(dpx - existing_y) >= min_distance for existing_y in down_point_xs):
            down_point_xs.append(dpx)
        if limit > 10000:
            down_point_xs=[]
            limit=0
            continue

    for i in range(num_flow):
        down_point = (down_point_xs[i],height+200)
        k, b = calculate_linear_function(up_point,down_point)
        current_point = [0,0]
        points = [up_point]

        for j in range(num_samples):
            step_length = int(np.random.normal((down_point[0]-up_point[0])/num_samples,5))
            print(i, j, step_length,down_point[0])
            new_x = current_point[0] + step_length
            mid_y = linear_function(k,b,(new_x))
            new_y = np.random.normal(mid_y,50)

            if new_y > height or len(points) >= num_samples:
                points.append(down_point)
                draw.line(points, fill='black', width=2)
                break
            new_point = (int(new_x), int(new_y))
            points.append(new_point)
            current_point = new_point

    return image


def segment_stream(stream_pts):
    left = stream_pts[0][0]
    right = stream_pts[-1][0]

    mode = np.random.randint(0,2)
    if mode == 0:
        # left Golden Section
        x = left + (right - left) * GR
        pred = []
        after = []
        ind = 0
        for pt in stream_pts:
            if pt[0] < x:
                pred = pt
                ind += 1
                continue
            if pt[0] > x:
                after = pt
                break

        k,b = calculate_linear_function(pred,after)
        y = linear_function(k,b,x)
        add_pt = [x,y]

        stream_pts = stream_pts[:ind]
        stream_pts.append(add_pt)
        return stream_pts

    elif mode == 1:
        pass
    
    


if __name__ == "__main__":
    num_segments =  2 # 折线条数
    num_samples = 5  # 每条折线段上的采样点数
    num_pulse = 1
    result_image,p, b, f = generate_line_segments(num_segments,num_samples,num_pulse)
    result_image.save(f'lines_image.png')
    

    # for i in tqdm.tqdm(range(100)):
    #     result_image = generate_perpendicular_tcp(num_segments, num_samples)
    #     result_image.save(f'./perpendicular/lines_image_{i}.png')
        