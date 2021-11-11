#pip install speedtest-cli
import speedtest
st=speedtest.Speedtest()
print(st.upload()*1.25e-7,"MB/s")
print(st.download()*1.25e-7,"MB/s")
print(st.results.ping)
