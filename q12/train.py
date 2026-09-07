import torch
from torch import nn

torch.manual_seed(20260907)
x = torch.linspace(-1, 1, 101).reshape(-1, 1)
y = 3 * x - 1
model = nn.Linear(1, 1)
loss_fn = nn.MSELoss()
opt = torch.optim.SGD(model.parameters(), lr=0.1)

for _ in range(200):
    pred = model(x)
    loss = loss_fn(pred, y)
    opt.zero_grad()      # TODO 1：清空上一轮的梯度
    loss.backward()      # TODO 2：反向传播，计算各参数梯度
    opt.step()           # TODO 3：按梯度更新参数

model.eval()             # TODO 4：进入评估模式（关闭 dropout/batchnorm 等）
with torch.no_grad():    # TODO 5：关闭梯度追踪，仅做前向推断
    pred = model(x)
    final_loss = loss_fn(pred, y)
    w = model.weight.item()
    b = model.bias.item()
    print(f"final loss = {final_loss.item():.6f}")
    print(f"weight = {w:.6f}, bias = {b:.6f}")
