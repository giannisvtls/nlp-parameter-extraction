from django.db import models
from channels.db import database_sync_to_async
from api.models import User
import random
import string

class UserService:
    @database_sync_to_async
    def create_user(self, name, initial_balance=0):
        """
        Asynchronously create a new user with IBAN and balance
        Returns tuple of (user, message)
        """
        try:
            # Check if user with name already exists
            if User.objects.filter(name=name).exists():
                return None, "User with this name already exists"
            
            # Generate IBAN and check if it exists
            while True:
                iban = self.generate_iban()
                if not User.objects.filter(iban=iban).exists():
                    break
            
            user = User.objects.create(
                name=name,
                iban=iban,
                balance=initial_balance
            )
            return user, "User created successfully"
        except Exception as e:
            return None, str(e)

    @database_sync_to_async
    def transfer_money(self, from_user, amount, to_iban):
        """
        Transfer money from one user to another using IBAN
        Returns tuple of (success, message)
        """
        try:
            # Validate amount
            if amount <= 0:
                return False, "Amount must be positive"

            # Check if sender has sufficient balance
            if from_user.balance < amount:
                return False, "Insufficient balance"

            # Find recipient by IBAN
            try:
                to_user = User.objects.get(iban=to_iban)
            except User.DoesNotExist:
                return False, "Recipient IBAN not found"

            # Don't allow transfers to self
            if from_user.iban == to_iban:
                return False, "Cannot transfer to self"

            # Use transaction.atomic() to ensure both operations succeed or fail together
            with transaction.atomic():
                # Deduct from sender
                from_user.balance -= amount
                from_user.save()

                # Add to recipient
                to_user.balance += amount
                to_user.save()

            return True, f"Successfully transferred {amount} to {to_user.name}"

        except Exception as e:
            return False, f"Transfer failed: {str(e)}"
    
    @database_sync_to_async
    def withdraw(self, username, amount):
        """
        Withdraw money from user's balance
        Returns tuple of (success, message)
        """
        try:
            # Validate amount
            if amount <= 0:
                return False, "Withdrawal amount must be positive"

            try:
                with transaction.atomic():
                    user = User.objects.select_for_update().get(name=username)
                    
                    # Check sufficient balance
                    if user.balance < amount:
                        return False, "Insufficient balance"
                    
                    # Perform withdrawal
                    user.balance -= amount
                    user.save()
                    
                    return True, f"Successfully withdrew {amount}. New balance: {user.balance}"
                    
            except User.DoesNotExist:
                return False, f"User {username} not found"

        except Exception as e:
            return False, f"Withdrawal failed: {str(e)}"

    @database_sync_to_async
    def deposit(self, username, amount):
        """
        Deposit money to user's balance
        Returns tuple of (success, message)
        """
        try:
            # Validate amount
            if amount <= 0:
                return False, "Deposit amount must be positive"

            try:
                with transaction.atomic():
                    user = User.objects.select_for_update().get(name=username)
                    
                    # Perform deposit
                    user.balance += amount
                    user.save()
                    
                    return True, f"Successfully deposited {amount}. New balance: {user.balance}"
                    
            except User.DoesNotExist:
                return False, f"User {username} not found"

        except Exception as e:
                return False, f"Deposit failed: {str(e)}"
    
    def generate_iban(self):
        """
        Generate a random IBAN
        Format: GR + 2 check digits + 3 bank code + 4 branch code + 16 account number
        """
        # Country code for Greece
        country_code = "GR"
        
        # Generate random numbers for each part
        check_digits = ''.join(random.choices(string.digits, k=2))
        bank_code = ''.join(random.choices(string.digits, k=3))
        branch_code = ''.join(random.choices(string.digits, k=4))
        account_number = ''.join(random.choices(string.digits, k=16))
        
        return f"{country_code}{check_digits}{bank_code}{branch_code}{account_number}"