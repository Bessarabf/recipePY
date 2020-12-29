
# читаем файл
data = loadtxt('surf.dat',skiprows=1)

nrow=shape(data)[0]
nrow

its,ids=37,73


x=linspace(0,360,ids)
y=linspace(-90,90,its)
z=zeros(its*ids).reshape(its,ids)
shape(z)

k=0
print k,ids,its
for j in range(ids):
    for i in range(its):
        z[its-i-1,j]=data[k,2]  # обратный порядок широты
        
        k=k+1
        

contourf(x,y,z)


