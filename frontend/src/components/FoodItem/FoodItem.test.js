import { fireEvent, render, screen } from '@testing-library/react';
import FoodItem from '.';
import OrderContext from '../../context/OrderContext';

describe('FoodItem', () => {
  const food = { id: 1, name: 'Test burger' };
  const addItem = jest.fn();

  beforeEach(() => {
    addItem.mockClear();
  });

  test('does not allow adding zero or negative quantities', () => {
    render(
      <OrderContext.Provider value={{ addItem }}>
        <FoodItem food={food} />
      </OrderContext.Provider>
    );

    const decrease = screen.getByRole('button', {
      name: 'Decrease Test burger quantity',
    });
    fireEvent.click(decrease);

    expect(screen.getByText('0')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Add to order' })).toBeDisabled();
  });

  test('adds the selected positive quantity', () => {
    render(
      <OrderContext.Provider value={{ addItem }}>
        <FoodItem food={food} />
      </OrderContext.Provider>
    );

    fireEvent.click(
      screen.getByRole('button', { name: 'Increase Test burger quantity' })
    );
    fireEvent.click(screen.getByRole('button', { name: 'Add to order' }));

    expect(addItem).toHaveBeenCalledWith(food, 1);
  });
});
