import React, { ReactElement } from 'react'
import classnames from 'classnames/bind'
import styles from './maincard.module.scss'
const cx = classnames.bind(styles)

type MainCardProps = {
    className?:string
    title: string
    element?: ReactElement
}

export default function MainCard({ className, title, element}: MainCardProps) {
    return (
        <div className={cx('box', className)}>
            <div className={cx('title')}>{title}</div>
            <div className={cx('body')}>
                {element}
            </div>
        </div>
    )
}
