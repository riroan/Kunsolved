import React, { ReactElement } from 'react'
import styles from './itemset.module.scss'
import classnames from 'classnames/bind'
const cx = classnames.bind(styles)

type ItemSetProps = {
    data?: ReactElement[]
}

export default function ItemSet({ data }: ItemSetProps) {
    return (
        <div className={cx('main')}>
            <ul className={cx('ul')}>
                {data}
            </ul>
        </div>
    )
}
