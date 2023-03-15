<template>
<div class="home">
  <div class="stat">

    <!--系统统计数据概览-->
    <div class="stat-info">
      <el-row :gutter="20" v-for="(info, index) in stat" :key="index">
        <el-col :span="8" v-for="(item, index) in info" :key="index">
          <div class="stat-info__item">
            <div class="stat-info__icon" :style="{'background-color': item.bgColor}">
              <i :class="item.icon"></i>
            </div>
            <div class="stat-info__detail">
              <p class="stat-info__total">{{item.total}}</p>
              <p class="stat-info__title">{{item.title}}</p>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

  </div>

  <!-- echarts部分-->
  <div id="line1" class="chart"></div>

</div>
</template>

<script>
  import Util from '@/assets/js/util';
  import 'echarts-liquidfill';

  export default {
    name: "Home",
    data() {
      return {
        host:'http://101.35.247.14:8000',
        token:localStorage.token,
        username:localStorage.username,
        userid:localStorage.user_id,

        stat: [
          [
            // {
            //   'title': '',
            //   'bgColor': '',
            //   'total': '',
            // }
          ],

        ],

      }
    },
    computed:{
      chartLine1() {
        return this.$echarts.init(Util.getDom('line1'));
      }
    },
    methods: {
      getOrderCount(){
        this.$axios.get(this.host +'/statistics/time_order_count/',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{

          this.drawLine1(response.data);

        }).catch(error=>{
          console.log(error.response);
        })
      },
      drawLine1(data)
      {


        let title = "今日和昨日评论量";
        let option = {
          title: Object.assign({}, Util.defaultEchartsOpt.title, {text: title}),
          grid: {
            top: 60,
            left: 60,
            right: 80,
            bottom: 20,
            containLabel: true
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              lineStyle: {
                color: '#ddd'
              }
            },
            backgroundColor: 'rgba(255,255,255,1)',
            padding: [5, 10],
            textStyle: {
              color: '#999',
            },
            extraCssText: 'box-shadow: 0 0 5px rgba(0,0,0,0.3)'
          },
          legend: {
            top: 15,
            right: 20,
            orient: 'vertical',
            textStyle: {
              color: "#666"
            }
          },
          xAxis: {
            type: 'category',
            data: ['00:00','2:00','4:00','6:00','8:00','10:00','12:00','14:00','16:00','18:00','20:00','22:00'],
            boundaryGap: false,
            splitLine: {
              show: false,
              interval: 'auto',
              lineStyle: {
                color: ['#D4DFF5']
              }
            },
            axisTick: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#999'
              }
            },
            axisLabel: {
              margin: 10,
              textStyle: {
                fontSize: 14
              }
            }
          },
          yAxis: {
            type: 'value',
            splitLine: {
              lineStyle: {
                color: ['#D4DFF5']
              }
            },
            axisTick: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#999'
              }
            },
            axisLabel: {
              margin: 10,
              textStyle: {
                fontSize: 14
              }
            }
          },
          series: [{
            name: '今日',
            type: 'line',
            smooth: true,
            showSymbol: false,
            symbol: 'circle',
            symbolSize: 4,
            data: data['t_count_list'],
            areaStyle: {
              normal: {
                color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                  offset: 0,
                  color: 'rgba(199, 237, 250,0.5)'
                }, {
                  offset: 1,
                  color: 'rgba(199, 237, 250,0.2)'
                }], false)
              }
            },
            itemStyle: {
              normal: {
                color: 'rgba(154, 116, 179, 0.7)'
              }
            },
            lineStyle: {
              normal: {
                width: 2
              }
            }
          }, {
            name: '昨日',
            type: 'line',
            smooth: true,
            showSymbol: false,
            symbol: 'circle',
            symbolSize: 4,
            data: data['y_count_list'],
            areaStyle: {
              normal: {
                color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                  offset: 0,
                  color: 'rgba(216, 244, 247,1)'
                }, {
                  offset: 1,
                  color: 'rgba(216, 244, 247,1)'
                }], false)
              }
            },
            itemStyle: {
              normal: {
                color: 'rgba(126, 237, 238, 0.7)'
              }
            },
            lineStyle: {
              normal: {
                width: 2
              }
            }
          }]
        };
        this.chartLine1.setOption(option);
        return this;
      },
      day_active_count(){
        // 获取日活跃用户总数
        this.$axios.get(this.host+'/statistics/day_active/',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.stat[0].splice(0,0,{
              title: '日活跃用户总数',
              total: response.data.count,
              bgColor: '#67c4ed'
            });
        }).catch(error=>{
          console.log(error.response);
        });

      },
      day_increment_count(){
        // 获取日增用户总数
        this.$axios.get(this.host+'/statistics/day_increment/',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.stat[0].splice(0,0,{
              title: '日增用户总数',
              total: response.data.count,
              bgColor: '#3acaa9'
            });
        }).catch(error=>{
          console.log(error.response);
        });


      },
      total_user_count(){
        // 获取用户总数
        this.$axios.get(this.host+'/statistics/total_count/',{
          headers:{
            // 固定的 格式 'JWT ' 一定要加空格
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.stat[0].splice(0,0,{
              title: '用户总数',
              total: response.data.count,
              bgColor: '#ebcc6f'
            });
        }).catch(error=>{
          console.log(error.response);
        });


      },


    },
    mounted() {
      this.total_user_count();
      this.day_increment_count();
      this.day_active_count();
      this.getOrderCount();
    }
  }
</script>

<style scoped lang="less">
  .home {
    height: calc(~'100% - 40px');
  }
  .stat {
    display: flex;
    height: 230px;
  }

  .stat-user__title {
    height: 100px;
    background-color: @mainColor;
    color: white;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    line-height: 70px;
  }
  .stat-user__detail {
    padding-top: 50px;
    color: #666;
    font-size: 13px;
    text-align: center;
  }
  .stat-user__portrait {
    position: absolute;
    top: 50%;
    left: 50%;
    .circle(80px);
    border: 3px solid white;
    box-shadow: 0 0 5px #ccc;
    margin-top: -55px;
    margin-left: -40px;
  }
  .stat-info {
    flex: 1;
    margin-left: 20px;
  }
  .el-row + .el-row {
    margin-top: 10px;
  }
  .stat-info__item {
    display: flex;
    height: 110px;
    box-shadow: 2px 2px 5px #ccc;
    background-color: @boxBgColor;
  }
  .stat-info__icon {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 80px;
    color: white;
    [class*='el-icon'] {
      font-size: 50px;
    }
  }
  .stat-info__detail {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .stat-info__total {
    color: #0085d0;
    font-size: 27px;
    font-weight: bold;
  }
  .stat-info__title {
    color: #666;
    font-size: 12px;
  }
  .list {
    display: flex;
    height: calc(~'100% - 250px');
    .el-col {
      height: 100%;
    }
  }
  .el-card {
    height: 100%;
    background-color: @boxBgColor;
    .el-icon-plus {
      float: right;
      color: @dangerColor;
      font-weight: bold;
      cursor: pointer;
    }
  }
  .el-card__header span {
    color: @subColor;
  }
  .el-card__body {
    p {
      border-bottom: 1px solid #e5e5e5;
      color: #555;
      font-size: 15px;
      line-height: 30px;
    }
    .active {
      color: #666;
      text-decoration: line-through;
    }
  }
  .latest-new-list__time {
    color: #666;
    font-size: 14px;
  }


  .chart {
    width: 100%;
    height: 350px;
    .border-radius(8px);
    background-color: @boxBgColor;
    box-shadow: 0 0 5px transparent;
    &:hover {
      box-shadow: 0 0 5px @mainColor;
    }
  }
</style>
