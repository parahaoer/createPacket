# 1、Linux系统下发送变长数据包
# 仅改变Linux系统发出的ICMP报文的负载长度，发送长度为0~100字节的数据包。
# 2、Linux系统下发送即变长又变内容
# 假定模式p的长度为|p|, ICMP负载长度为|s|. 其中 模式p的最大长度位16字节。
# 分别发送负载长度|s|为0~3|p|的报文，以及|s|为10|p|的报文

host=192.168.222.1
#read -p "enter dest host：" host
for i in {0..100}
do
ping -s $i -c 1 $host
done

pattern_array=("01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13" "14" "15" "16")

for p_len in {1..16}
do
    
    for((i=1;i<=$p_len;i++));  
    do
        p=$p${pattern_array[$i-1]}
    done     

    echo $p

    for((s_len=0;s_len<=3*$p_len;s_len++));  
    do     
        ping $host -p $p -s $s_len -c 1
    done
    echo 10*$p_len
    ping $host -p $p -s `expr 10 \* $p_len` -c 1
    # 每一个长度的pattern的数据包发送完后， 重新将 pattern置为空串。
    p=""

done