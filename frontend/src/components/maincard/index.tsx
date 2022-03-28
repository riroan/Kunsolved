import React, { ReactElement } from 'react'
import classnames from 'classnames/bind'
import styles from './maincard.module.scss'
const cx = classnames.bind(styles)

type MainCardProps = {
    title: string
    leftElement: ReactElement
    rightElement?: ReactElement
}

export default function MainCard({ title, leftElement, rightElement }: MainCardProps) {
    return (
        <div className={cx('box')}>
            <div className={cx('title')}>{title}</div>
            <div className={cx('body')}>
                <div className={cx('left')}>{leftElement}</div>
                <div className={cx('right')}>{rightElement}</div>
            </div>
        </div>
    )
}
