import { useState, useContext } from 'react';
import style from './FoodItem.module.scss';
import OrderContext from '../../context/OrderContext';

export default function FoodItem({ food }) {
  const [quantity, setQuantity] = useState(0);
  const { addItem } = useContext(OrderContext);

  return (
    <div className={style.wrapper}>
      <div>{food.name}</div>
      <div className={style.actionWrapper}>
        <div className={style.action}>
          <button
            type='button'
            aria-label={`Decrease ${food.name} quantity`}
            onClick={() => setQuantity((current) => Math.max(0, current - 1))}
          >
            -
          </button>
          {quantity}
          <button
            type='button'
            aria-label={`Increase ${food.name} quantity`}
            onClick={() => setQuantity((current) => current + 1)}
          >
            +
          </button>
        </div>

        <button
          className={style.button}
          disabled={quantity < 1}
          onClick={() => {
            addItem(food, quantity);
          }}
        >
          Add to order
        </button>
      </div>
    </div>
  );
}
