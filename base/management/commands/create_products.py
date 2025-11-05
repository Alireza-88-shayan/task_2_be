from django.core.management.base import BaseCommand
from base.models import Product, Category, ProductFeatures
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import random

class Command(BaseCommand):
    help = 'Create sample products'

    def handle(self, *args, **kwargs):
        categories = Category.objects.all()
        features = ProductFeatures.objects.all()

        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found. Please create some first.'))
            return

        if not features.exists():
            self.stdout.write(self.style.ERROR('No product features found. Please create some first.'))
            return

        colors = ['0', '1', '2', '3']

        for i in range(50):
            product = Product.objects.create(
                title=f'محصول شماره {i+1}',
                describtion='توضیحات تست برای محصول',
                price=random.randint(100000, 1000000),
                color=random.choice(colors),
                is_available=True,
                rate=round(random.uniform(1, 5), 1),
                discount=random.choice([0, 10, 20, 30]),
                category=random.choice(categories)
            )

            # Assign random features
            product.productFeatures.set(random.sample(list(features), k=min(3, len(features))))

            # Generate a dummy image
            image = Image.new('RGB', (300, 300), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            buffer = BytesIO()
            image.save(buffer, format='JPEG')
            product.image.save(f'product_{i+1}.jpg', ContentFile(buffer.getvalue()), save=True)

            self.stdout.write(self.style.SUCCESS(f'Created product: {product.title}'))

        self.stdout.write(self.style.SUCCESS('All products created successfully.'))
