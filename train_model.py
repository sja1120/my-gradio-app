import os
import torch
from torch import nn, optim
from torchvision import datasets, transforms, models

# 1. 데이터셋 위치
data_dir = "waste_dataset"

# 2. 전처리 정의
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# 3. 데이터 불러오기
dataset = datasets.ImageFolder(data_dir, transform=transform)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=8, shuffle=True)

# 4. 라벨 정보 저장
class_names = dataset.classes
with open("labels.txt", "w", encoding="utf-8") as f:
    for label in class_names:
        f.write(label + "\n")

# 5. 사전학습된 모델 불러오기 (MobileNetV2)
model = models.mobilenet_v2(pretrained=True)
model.classifier[1] = nn.Linear(model.last_channel, len(class_names))

# 6. 학습 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 7. 학습 루프
epochs = 5
for epoch in range(epochs):
    model.train()
    running_loss = 0
    for images, labels in dataloader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(dataloader):.4f}")

# 8. 모델 저장
torch.save(model.state_dict(), "waste_classifier.pth")
print("✅ 모델 저장 완료: waste_classifier.pth")