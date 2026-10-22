import axios from 'axios';
import { useContext, useEffect, useState } from 'react';
import OrderContext from '../../context/OrderContext';
import { API_URL } from '../../utils/constants';
import style from './Order.module.scss';

export default function Order() {
  const { orderName, orderItems } = useContext(OrderContext);
  const [deliveryDistance, setDeliveryDistance] = useState(0);
  const [deliveryFee, setDeliveryFee] = useState(0);
  const [subtotal, setSubtotal] = useState(0);
  const [tax, setTax] = useState(0);
  const [total, setTotal] = useState(0);
  const [loadError, setLoadError] = useState('');

  const renderItem = (orderItem, idx) => {
    return (
      <div className={style.itemWrapper} key={idx}>
        <span className={style.item}>{orderItem.item}</span>
        <span>{orderItem.quantity}</span>
      </div>
    );
  };

  const renderDelivery = () => {
    return (
      <div className={style.itemWrapper}>
        <span className={style.item}>What's your distance?</span>
        <select
          value={deliveryDistance}
          onChange={(event) => {
            setDeliveryDistance(event.target.value);
          }}
        >
          <option value='0'></option>
          <option value='1'>1 mile</option>
          <option value='3'>3 miles</option>
          <option value='5'>5 miles</option>
          <option value='10'>10 miles</option>
        </select>
      </div>
    );
  };

  const renderFee = (name, cost) => {
    // Create our number formatter.
    var formatter = new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',

      // These options are needed to round to whole numbers if that's what you want.
      //minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
      //maximumFractionDigits: 0, // (causes 2500.99 to be printed as $2,501)
    });

    return (
      <div className={style.itemWrapper}>
        <span className={style.item}>{name}</span>
        <span>{formatter.format(cost)}</span>
      </div>
    );
  };

  useEffect(() => {
    let active = true;
    const loadTotals = async () => {
      try {
        const [delivery, subtotalResponse, taxResponse, totalResponse] =
          await Promise.all([
            axios.get(
              `${API_URL}/api/delivery/${orderName}/${deliveryDistance}`
            ),
            axios.get(`${API_URL}/api/subtotal/${orderName}`),
            axios.get(`${API_URL}/api/tax/${orderName}/${deliveryDistance}`),
            axios.get(`${API_URL}/api/total/${orderName}/${deliveryDistance}`),
          ]);

        const responses = [
          delivery,
          subtotalResponse,
          taxResponse,
          totalResponse,
        ];
        if (responses.some((response) => response.data.status !== 'success')) {
          if (active) {
            setLoadError('The server could not calculate the order totals.');
          }
          return;
        }

        if (active) {
          setDeliveryFee(delivery.data.data);
          setSubtotal(subtotalResponse.data.data);
          setTax(taxResponse.data.data);
          setTotal(totalResponse.data.data);
          setLoadError('');
        }
      } catch (error) {
        if (!axios.isAxiosError(error)) {
          throw error;
        }
        if (active) {
          setLoadError('Unable to load order totals. Please try again.');
        }
      }
    };

    loadTotals();
    return () => {
      active = false;
    };
  }, [deliveryDistance, orderName]);
  return (
    <div className={style.wrapper}>
      {loadError && <p role='alert'>{loadError}</p>}
      {orderItems.length > 0 && renderDelivery()}
      <h3>Your Order</h3>
      {orderItems.map((orderItem, idx) => renderItem(orderItem, idx))}
      {renderFee('Subtotal', subtotal)}
      {renderFee('Delivery Fee', deliveryFee)}
      {renderFee('Tax', tax)}
      <div className={style.bottomLine}>{renderFee('Total', total)}</div>
    </div>
  );
}
