
from typing import Optional
from LinkedList import ListNode


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        
        ans = ListNode(0)
        l3 = ans
        carry = 0
        while l1 or l2 or carry:
            val1 = 0
            if l1.val is not None:
                val1 = l1.val

            val2 = 0
            if l2.val is not None:
                val2 = l2.val
           
            out = (val1 + val2 + carry) % 10
            
            if (val1 + val2 + carry) >= 10:
                carry = 1
            else:
                carry = 0
          
            l3.val = out

            l3.next = ListNode(0)
            l3 = l3.next
            
            l1 = (l1.next if l1 else None) # 當 if 的條件成立的時候, 就給if的值, 否則給 else 後面的值
            l2 = (l2.next if l2 else None)

        return ans

# Example usage:
l1 = ListNode(2, ListNode(4, ListNode(3)))
l2 = ListNode(5, ListNode(6, ListNode(4)))
solution = Solution()
result = solution.addTwoNumbers(l1, l2)
while result:
    print(result.val)  # Output: 7 -> 0 -> 8  
    result = result.next