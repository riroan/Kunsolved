import React, { useState, useEffect, ReactElement } from 'react'
import classnames from 'classnames/bind'
import styles from './navigation.module.scss'
import color, { tier2color } from '../_config/color'
import { PieChart } from 'react-minimal-pie-chart'
import { DataEntry } from 'react-minimal-pie-chart/types/commonTypes'
import MainCard from '../maincard/index'
import RadarChart from 'react-svg-radar-chart'
const cx = classnames.bind(styles)

export default function Navigation() {
    const [data, setData] = useState<DataEntry[]>([])
    const [count, setCount] = useState<ReactElement[]>([])
    const [exp, setExp] = useState({})
    const caption = {
        math: '수학',
        implementation: '구현',
        greedy: '그리디',
        string: '문자열',
        data_structures: '자료구조',
        graphs: '그래프',
        dp: 'DP',
        geometry: '기하학',
    }
    const options = {
    }

    useEffect(() => {
        var url = 'http://localhost:8000/byLevel'
        fetch(url, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then(res => res.json())
            .then(res => {
                var sum = 0
                var pieData = []
                var countData = []
                for (var d in res) {
                    sum += res[d]
                }
                for (d in res) {
                    const value = (res[d] / sum) * 100
                    const tierColor = tier2color(parseInt(d), false)
                    pieData.push({ title: tierColor, value: value, color: color[tierColor] })
                    countData.push(
                        <li style={{ display: 'flex', alignItems: 'center' }}>
                            <div style={{ width: '10px', height: '10px', background: color[tierColor], marginRight: '5px' }}></div>
                            {res[d]}
                        </li>
                    )
                }
                setCount(countData)
                setData(pieData)
            })
        // url = 'http://localhost:8000/byTag?tags=수학&tags=구현&tags=문자열&tags=그리디%20알고리즘&tags=다이나믹%20프로그래밍&tags=그래프%20이론&tags=기하학&tags=자료%20구조'
        // url = 'http://localhost:8000/byTag?tags=수학&value=cnt'
        // fetch(url, {
        //     method: 'GET',
        //     headers: {
        //         Accept: 'application/json',
        //         'Content-Type': 'application/json',
        //     },
        // })
        //     .then(res => res.json())
        //     .then(res => {
        //         console.log(res)
        //     })
    }, [])
    return (
        <div>
            <MainCard
                title="건국대학교 티어별 해결한 문제 수"
                leftElement={
                    <PieChart
                        style={{
                            fontFamily: '"Nunito Sans", -apple-system, Helvetica, Arial, sans-serif',
                            fontSize: '5px',
                            width: '300px',
                        }}
                        radius={PieChart.defaultProps.radius - 6}
                        data={data}
                        startAngle={-90}
                        segmentsStyle={{ transition: 'stroke .3s', cursor: 'pointer' }}
                        animate
                        animationDuration={500}
                    />
                }
                rightElement={<ul>{count}</ul>}
            />
            <MainCard
                title="건국대학교 주요 태그 분포(해결 수)"
                leftElement={
                    <div>
                        <RadarChart
                            captions={caption}
                            data={[
                                // data
                                {
                                    data: {
                                        math: 0.95,
                                        greedy: 0.25,
                                        string: 0.36,
                                        data_structures: 0.36,
                                        geometry: 0.11,
                                        dp: 0.39,
                                        implementation: 1.0,
                                        graphs: 0.45
                                    },
                                    meta: { color: '#58FCEC' },
                                },
                            ]}
                            size={300}
                            options={options}
                        />
                    </div>
                }
            />
        </div>
    )
}
