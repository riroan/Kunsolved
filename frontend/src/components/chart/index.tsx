import React, { useState } from 'react'
import { PieChart } from 'react-minimal-pie-chart'
import styles from './chart.module.scss'
import classnames from 'classnames/bind'
import {  DataEntry } from 'react-minimal-pie-chart/types/commonTypes'
const cx = classnames.bind(styles)

type ChartProps = {
    data:DataEntry[]
}

export default function Chart({ data} : ChartProps ) {
    return (
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
    )
}
